const { app, BrowserWindow } = require('electron');
const path = require('path');

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: { nodeIntegration: true, contextIsolation: false }
  });
  win.loadURL(process.env.ELECTRON_START_URL || `file://${path.join(__dirname, '../dist/index.html')}`);
}
app.whenReady().then(createWindow);

