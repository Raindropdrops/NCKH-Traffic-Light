#!/usr/bin/env python3
"""
Experiment Runner - Traffic Light MQTT Demo
Runs all experiment cases and generates summary report.

Usage:
    python run_experiments.py --host 192.168.1.100
    python run_experiments.py --host 192.168.1.100 --output-dir ../results/run_001
"""

import argparse
import csv
import os
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import pandas as pd


@dataclass
class ExperimentCase:
    name: str
    pad_bytes: int
    count: int
    interval_ms: int
    mode: str = "AUTO"
    description: str = ""


# Define experiment cases
EXPERIMENT_CASES = [
    ExperimentCase(
        name="case1",
        pad_bytes=0,
        count=500,
        interval_ms=200,
        description="Baseline (no padding)"
    ),
    ExperimentCase(
        name="case2",
        pad_bytes=256,
        count=500,
        interval_ms=200,
        description="Medium payload (256B padding)"
    ),
    ExperimentCase(
        name="case3",
        pad_bytes=1024,
        count=500,
        interval_ms=200,
        description="Large payload (1024B padding)"
    ),
]


def run_case(case: ExperimentCase, host: str, port: int, user: str, password: str,
             output_dir: Path) -> Optional[Path]:
    """Run a single experiment case."""
    output_file = output_dir / f"results_{case.name}.csv"
    
    print(f"\n{'='*60}")
    print(f"📊 Running {case.name}: {case.description}")
    print(f"   pad_bytes={case.pad_bytes}, count={case.count}, interval={case.interval_ms}ms")
    print(f"   Output: {output_file}")
    print(f"{'='*60}")
    
    # Build command
    cmd = [
        sys.executable, "logger.py",
        "--host", host,
        "--port", str(port),
        "--user", user,
        "--password", password,
        "--count", str(case.count),
        "--interval_ms", str(case.interval_ms),
        "--mode", case.mode,
        "--pad_bytes", str(case.pad_bytes),
        "--out", str(output_file)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=False, text=True)
        if result.returncode == 0:
            print(f"✅ {case.name} completed successfully")
            return output_file
        else:
            print(f"❌ {case.name} failed with code {result.returncode}")
            return None
    except Exception as e:
        print(f"❌ {case.name} error: {e}")
        return None


def analyze_case(csv_file: Path, histogram: bool = True) -> Optional[dict]:
    """Analyze a single case result."""
    if not csv_file.exists():
        return None
    
    try:
        df = pd.read_csv(csv_file)
        rtts = df['rtt_ms'].dropna()
        
        if len(rtts) == 0:
            return {
                'file': csv_file.name,
                'sent': len(df),
                'received': 0,
                'lost': len(df),
                'loss_rate': 100.0,
                'min': None,
                'max': None,
                'mean': None,
                'median': None,
                'std': None,
                'p95': None,
                'p99': None,
                'status': 'FAIL',
                'reason': 'Timeout/no-ack'
            }
        
        stats = {
            'file': csv_file.name,
            'sent': len(df),
            'received': len(rtts),
            'lost': len(df) - len(rtts),
            'loss_rate': ((len(df) - len(rtts)) / len(df) * 100) if len(df) > 0 else 0,
            'min': rtts.min(),
            'max': rtts.max(),
            'mean': rtts.mean(),
            'median': rtts.median(),
            'std': rtts.std(),
            'p95': rtts.quantile(0.95),
            'p99': rtts.quantile(0.99),
            'status': 'PASS' if ((len(df) - len(rtts)) / len(df) * 100) < 1 else 'FAIL',
            'reason': '' if ((len(df) - len(rtts)) / len(df) * 100) < 1 else 'Loss >= 1%'
        }
        
        # Generate histogram
        if histogram:
            try:
                import matplotlib.pyplot as plt
                
                hist_dir = csv_file.parent / "histograms"
                hist_dir.mkdir(exist_ok=True)
                hist_file = hist_dir / f"{csv_file.stem}_histogram.png"
                
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.hist(rtts, bins=50, edgecolor='black', alpha=0.7, color='steelblue')
                ax.axvline(rtts.mean(), color='red', linestyle='--', linewidth=2, 
                          label=f'Mean: {rtts.mean():.1f}ms')
                ax.axvline(rtts.quantile(0.95), color='orange', linestyle='--', linewidth=2,
                          label=f'P95: {rtts.quantile(0.95):.1f}ms')
                ax.set_xlabel('RTT (ms)')
                ax.set_ylabel('Frequency')
                ax.set_title(f'RTT Distribution - {csv_file.stem}')
                ax.legend()
                ax.grid(True, alpha=0.3)
                
                plt.tight_layout()
                plt.savefig(hist_file, dpi=150)
                plt.close()
                
                stats['histogram'] = str(hist_file)
            except ImportError:
                pass
        
        return stats
        
    except Exception as e:
        print(f"❌ Analysis error for {csv_file}: {e}")
        return None


def generate_summary(results: List[dict], output_dir: Path):
    """Generate summary CSV and Markdown report."""
    if not results:
        print("❌ No results to summarize")
        return
    
    # CSV Summary
    csv_file = output_dir / "summary.csv"
    df = pd.DataFrame(results)
    df.to_csv(csv_file, index=False)
    print(f"\n💾 Summary CSV: {csv_file}")
    
    # Markdown Summary
    md_file = output_dir / "summary.md"
    
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write("# 📊 Experiment Results Summary\n\n")
        f.write(f"> Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("---\n\n")
        
        f.write("## Results Table\n\n")
        f.write("| Case | Sent | Recv | Lost | Loss% | Min | Mean | Median | P95 | P99 | Max | Status | Lý do |\n")
        f.write("|------|------|------|------|-------|-----|------|--------|-----|-----|-----|--------|------|\n")

        def md_metric(value):
            return "N/A" if value is None else f"{value:.1f}"
        
        for r in results:
            f.write(f"| {r['file']} | {r['sent']} | {r['received']} | {r['lost']} | ")
            f.write(f"{r['loss_rate']:.2f}% | {md_metric(r['min'])} | {md_metric(r['mean'])} | ")
            f.write(f"{md_metric(r['median'])} | {md_metric(r['p95'])} | {md_metric(r['p99'])} | {md_metric(r['max'])} | ")
            f.write(f"{r.get('status', 'N/A')} | {r.get('reason', '-') or '-'} |\n")
        
        f.write("\n---\n\n")
        
        # Threshold validation
        f.write("## Threshold Validation\n\n")
        f.write("| Case | Mean < 200ms | P95 < 500ms | Loss < 1% | Overall | Lý do |\n")
        f.write("|------|--------------|-------------|-----------|----------|------|\n")
        
        for r in results:
            mean_ok = "✅" if r['mean'] is not None and r['mean'] < 200 else "❌"
            p95_ok = "✅" if r['p95'] is not None and r['p95'] < 500 else "❌"
            loss_ok = "✅" if r['loss_rate'] < 1 else "❌"
            if r['mean'] is None or r['p95'] is None:
                overall = "❌ FAIL"
                reason = "Timeout/no-ack"
            elif r['mean'] < 200 and r['p95'] < 500 and r['loss_rate'] < 1:
                overall = "✅ PASS"
                reason = "-"
            else:
                overall = "❌ FAIL"
                reason = "Thresholds not met"
            f.write(f"| {r['file']} | {mean_ok} | {p95_ok} | {loss_ok} | {overall} | {reason} |\n")
        
        f.write("\n---\n\n")
        
        # Histograms
        if any('histogram' in r for r in results):
            f.write("## Histograms\n\n")
            for r in results:
                if 'histogram' in r:
                    hist_path = Path(r['histogram']).name
                    f.write(f"### {r['file']}\n\n")
                    f.write(f"![{r['file']}](histograms/{hist_path})\n\n")
    
    print(f"📝 Summary MD: {md_file}")


def main():
    parser = argparse.ArgumentParser(
        description='Run all RTT experiment cases',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_experiments.py --host 192.168.1.100
  python run_experiments.py --host localhost --output-dir ../results/run_001
  python run_experiments.py --host 192.168.1.100 --skip-run  # Analyze existing results
        """
    )
    
    parser.add_argument('--host', required=True, help='MQTT broker host')
    parser.add_argument('--port', type=int, default=1883, help='MQTT broker port')
    parser.add_argument('--user', default='demo', help='MQTT username')
    parser.add_argument('--password', default='demo_pass', help='MQTT password')
    parser.add_argument('--output-dir', default='../results', help='Output directory')
    parser.add_argument('--skip-run', action='store_true', help='Skip running, analyze existing')
    parser.add_argument('--no-histogram', action='store_true', help='Skip histogram generation')
    
    args = parser.parse_args()
    
    # Setup output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("🔬 EXPERIMENT RUNNER")
    print("=" * 60)
    print(f"  Host: {args.host}:{args.port}")
    print(f"  User: {args.user}")
    print(f"  Output: {output_dir.absolute()}")
    print(f"  Cases: {len(EXPERIMENT_CASES)}")
    print("=" * 60)
    
    # Run experiments
    csv_files = []
    
    if not args.skip_run:
        for case in EXPERIMENT_CASES:
            result = run_case(case, args.host, args.port, args.user, args.password, output_dir)
            if result:
                csv_files.append(result)
            
            # Small delay between cases
            import time
            time.sleep(2)
    else:
        # Find existing CSV files
        print("\n⏭️ Skipping run, analyzing existing results...")
        for case in EXPERIMENT_CASES:
            csv_file = output_dir / f"results_{case.name}.csv"
            if csv_file.exists():
                csv_files.append(csv_file)
    
    # Analyze results
    print(f"\n📊 Analyzing {len(csv_files)} result files...")
    results = []
    for csv_file in csv_files:
        stats = analyze_case(csv_file, histogram=not args.no_histogram)
        if stats:
            results.append(stats)
    
    # Generate summary
    generate_summary(results, output_dir)
    
    print("\n" + "=" * 60)
    print("🎉 EXPERIMENT COMPLETE")
    print("=" * 60)
    print(f"  Results: {output_dir.absolute()}")
    print(f"  Cases run: {len(csv_files)}")
    print(f"  Summary: summary.csv, summary.md")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
