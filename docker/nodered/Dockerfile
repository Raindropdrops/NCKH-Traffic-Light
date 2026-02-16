FROM nodered/node-red:latest

USER root
# Install build dependencies if needed (optional)
RUN apk add --no-cache make gcc g++ python3

USER node-red
# Install dashboard package
RUN npm install node-red-dashboard
# Install other useful nodes if requested
RUN npm install node-red-contrib-ui-led

# Fix persistence volume permission if necessary
# Note: entrypoint handles /data usually, but good to be safe
