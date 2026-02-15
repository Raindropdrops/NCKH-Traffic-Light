#!/usr/bin/env python3
"""
RTT Results Analyzer - Traffic Light MQTT Demo
Analyzes benchmark CSV results and generates statistics + optional histogram.

Usage:
    python analyze_results.py results.csv
    python analyze_results.py results.csv --histogram
    python analyze_results.py results.csv --threshold-mean 200 --threshold-p95 500
"""

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

# Optional matplotlib for histogram
try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False


def load_csv(filename: str) -> pd.DataFrame:
    """Load CSV file into DataFrame."""
    try:
        df = pd.read_csv(filename)
        print(f"📂 Loaded {len(df)} records from {filename}")
        return df
    except FileNotFoundError:
        print(f"❌ File not found: {filename}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error loading CSV: {e}")
        sys.exit(1)


def calculate_statistics(df: pd.DataFrame) -> dict:
    """Calculate comprehensive RTT statistics."""
    total = len(df)
    received = df['rtt_ms'].notna().sum()
    lost = total - received
    
    rtts = df['rtt_ms'].dropna()
    
    stats = {
        'total_sent': total,
        'total_received': received,
        'total_lost': lost,
        'loss_rate': (lost / total * 100) if total > 0 else 0,
    }
    
    if len(rtts) > 0:
        stats.update({
            'min': rtts.min(),
            'max': rtts.max(),
            'mean': rtts.mean(),
            'median': rtts.median(),
            'std': rtts.std(),
            'p50': rtts.quantile(0.50),
            'p75': rtts.quantile(0.75),
            'p90': rtts.quantile(0.90),
            'p95': rtts.quantile(0.95),
            'p99': rtts.quantile(0.99),
        })
    else:
        stats.update({
            'min': None, 'max': None, 'mean': None, 'median': None,
            'std': None, 'p50': None, 'p75': None, 'p90': None, 
            'p95': None, 'p99': None
        })
    
    return stats


def analyze_by_command(df: pd.DataFrame):
    """Analyze RTT grouped by command type."""
    if 'note' not in df.columns:
        return None
    
    grouped = df.groupby('note')['rtt_ms'].agg(['count', 'mean', 'median', 'std', 'max'])
    return grouped


def analyze_payload_impact(df: pd.DataFrame):
    """Analyze RTT vs payload size."""
    if 'payload_size' not in df.columns:
        return None
    
    df_valid = df[df['rtt_ms'].notna()].copy()
    if len(df_valid) == 0:
        return None
    
    # Group by payload size ranges
    df_valid['size_bucket'] = pd.cut(df_valid['payload_size'], 
                                      bins=[0, 100, 200, 500, 1000, float('inf')],
                                      labels=['0-100', '101-200', '201-500', '501-1000', '>1000'])
    
    grouped = df_valid.groupby('size_bucket', observed=True)['rtt_ms'].agg(['count', 'mean', 'p95'])
    return grouped


def print_statistics(stats: dict, thresholds: dict):
    """Print formatted statistics table."""
    print("\n" + "=" * 60)
    print("📊 RTT BENCHMARK ANALYSIS RESULTS")
    print("=" * 60)
    
    print("\n📈 DELIVERY STATISTICS")
    print("-" * 40)
    print(f"  Total Sent:     {stats['total_sent']:>10}")
    print(f"  Total Received: {stats['total_received']:>10}")
    print(f"  Total Lost:     {stats['total_lost']:>10}")
    print(f"  Loss Rate:      {stats['loss_rate']:>10.2f}%")
    
    if stats['mean'] is not None:
        print("\n📏 RTT DISTRIBUTION (ms)")
        print("-" * 40)
        print(f"  Min:            {stats['min']:>10.2f}")
        print(f"  Max:            {stats['max']:>10.2f}")
        print(f"  Mean:           {stats['mean']:>10.2f}")
        print(f"  Median:         {stats['median']:>10.2f}")
        print(f"  Std Dev:        {stats['std']:>10.2f}")
        
        print("\n📊 PERCENTILES (ms)")
        print("-" * 40)
        print(f"  P50 (Median):   {stats['p50']:>10.2f}")
        print(f"  P75:            {stats['p75']:>10.2f}")
        print(f"  P90:            {stats['p90']:>10.2f}")
        print(f"  P95:            {stats['p95']:>10.2f}")
        print(f"  P99:            {stats['p99']:>10.2f}")
        
        # Threshold checks
        print("\n✅ THRESHOLD VALIDATION")
        print("-" * 40)
        
        checks = []
        
        # Mean check
        mean_ok = stats['mean'] <= thresholds['mean']
        status = "✅ PASS" if mean_ok else "❌ FAIL"
        print(f"  Mean <= {thresholds['mean']}ms:    {status} ({stats['mean']:.2f}ms)")
        checks.append(mean_ok)
        
        # P95 check
        p95_ok = stats['p95'] <= thresholds['p95']
        status = "✅ PASS" if p95_ok else "❌ FAIL"
        print(f"  P95 <= {thresholds['p95']}ms:     {status} ({stats['p95']:.2f}ms)")
        checks.append(p95_ok)
        
        # Loss rate check
        loss_ok = stats['loss_rate'] <= thresholds['loss']
        status = "✅ PASS" if loss_ok else "❌ FAIL"
        print(f"  Loss <= {thresholds['loss']}%:      {status} ({stats['loss_rate']:.2f}%)")
        checks.append(loss_ok)
        
        print("\n" + "=" * 60)
        if all(checks):
            print("🎉 OVERALL: ALL THRESHOLDS PASSED")
        else:
            print("⚠️ OVERALL: SOME THRESHOLDS FAILED")
        print("=" * 60 + "\n")
        
        return all(checks)
    else:
        print("\n❌ No RTT data available (no acks received)")
        return False


def plot_histogram(df: pd.DataFrame, output_file: str):
    """Generate and save RTT histogram."""
    if not HAS_MATPLOTLIB:
        print("⚠️ matplotlib not installed. Skipping histogram.")
        return
    
    rtts = df['rtt_ms'].dropna()
    if len(rtts) == 0:
        print("⚠️ No RTT data for histogram")
        return
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Histogram
    ax1 = axes[0]
    ax1.hist(rtts, bins=50, edgecolor='black', alpha=0.7, color='steelblue')
    ax1.axvline(rtts.mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {rtts.mean():.1f}ms')
    ax1.axvline(rtts.quantile(0.95), color='orange', linestyle='--', linewidth=2, label=f'P95: {rtts.quantile(0.95):.1f}ms')
    ax1.set_xlabel('RTT (ms)')
    ax1.set_ylabel('Frequency')
    ax1.set_title('RTT Distribution')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Box plot
    ax2 = axes[1]
    bp = ax2.boxplot(rtts, vert=True, patch_artist=True)
    bp['boxes'][0].set_facecolor('lightblue')
    ax2.set_ylabel('RTT (ms)')
    ax2.set_title('RTT Box Plot')
    ax2.grid(True, alpha=0.3)
    
    # Add statistics text
    stats_text = f"n={len(rtts)}\nMean={rtts.mean():.1f}ms\nMedian={rtts.median():.1f}ms\nP95={rtts.quantile(0.95):.1f}ms"
    ax2.text(1.15, rtts.median(), stats_text, fontsize=9, verticalalignment='center')
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"📊 Histogram saved to: {output_file}")
    plt.close()


def main():
    parser = argparse.ArgumentParser(
        description='Analyze RTT benchmark results from CSV',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python analyze_results.py results.csv
  python analyze_results.py results.csv --histogram
  python analyze_results.py results.csv --threshold-mean 200 --threshold-p95 500 --threshold-loss 1.0
        """
    )
    
    parser.add_argument('csv_file', help='CSV file from logger.py')
    parser.add_argument('--histogram', action='store_true', help='Generate histogram PNG')
    parser.add_argument('--histogram-output', default=None, help='Histogram output filename')
    
    # Thresholds
    parser.add_argument('--threshold-mean', type=float, default=200, 
                        help='Maximum acceptable mean RTT (ms)')
    parser.add_argument('--threshold-p95', type=float, default=500, 
                        help='Maximum acceptable P95 RTT (ms)')
    parser.add_argument('--threshold-loss', type=float, default=1.0, 
                        help='Maximum acceptable loss rate (%%)')
    
    args = parser.parse_args()
    
    # Load data
    df = load_csv(args.csv_file)
    
    # Calculate statistics
    stats = calculate_statistics(df)
    
    # Define thresholds
    thresholds = {
        'mean': args.threshold_mean,
        'p95': args.threshold_p95,
        'loss': args.threshold_loss
    }
    
    # Print results
    passed = print_statistics(stats, thresholds)
    
    # Command breakdown
    cmd_stats = analyze_by_command(df)
    if cmd_stats is not None and len(cmd_stats) > 1:
        print("\n📋 RTT BY COMMAND TYPE")
        print("-" * 60)
        print(cmd_stats.to_string())
        print()
    
    # Generate histogram
    if args.histogram:
        hist_file = args.histogram_output or Path(args.csv_file).stem + '_histogram.png'
        plot_histogram(df, hist_file)
    
    # Exit code based on thresholds
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
