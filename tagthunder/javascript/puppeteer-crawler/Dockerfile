FROM node:16

# update and add all the steps for running with xvfb
RUN apt-get update
RUN apt-get -qq -y install curl
RUN apt-get install -yq gconf-service libasound2 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 \
libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 \
libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 \
libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 \
ca-certificates fonts-liberation libnss3 lsb-release xdg-utils wget \
xvfb x11vnc x11-xkb-utils xfonts-100dpi xfonts-75dpi xfonts-scalable xfonts-cyrillic x11-apps chromium
# add the required dependencies
WORKDIR /app
COPY node_modules /app/node_modules
COPY package.json /app/package.json
COPY extensions /app/extensions
COPY . . 
RUN npm install 

EXPOSE 8080

ENV DISPLAY :99
CMD Xvfb :99 -screen 0 1024x768x16 & node server.js

