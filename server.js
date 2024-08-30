const express = require('express');
const path = require('path');
const { spawn } = require('child_process');
const { promisify } = require('util');


const app = express();
const parseScriptPath = path.join(__dirname, "parse.py");
const port = 3000;

// Serve static files from the 'public' directory
app.use(express.static(path.join(__dirname, 'public')));

app.get("/api/files", (req, res) => {
  const dir = req.query.directory;

  // Validate the 'directory' parameter
  if (!dir) {
    return res.status(400).send("Directory parameter is required");
  }

  // Spawn the Python process
  const pythonProcess = spawn("python3", [parseScriptPath, dir, "--type", "files"]);

  // Collect data from stdout
  let result = '';
  pythonProcess.stdout.on('data', (data) => {
    result += data.toString();
  });

  // Handle errors from stderr
  pythonProcess.stderr.on('data', (data) => {
    console.error(`Python error: ${data}`);
  });

  // Handle process exit
  pythonProcess.on('close', (code) => {
    if (code !== 0) {
      return res.status(500).send(`Python script exited with code ${code}`);
    }

    try {
      // Parse and send the result
      const parsedResult = JSON.parse(result.replace(/'/g, "\""));
      console.log(parsedResult)

      res.status(200).json(parsedResult);
    } catch (e) {
      console.error(`Error parsing JSON: ${e}`);
      res.status(500).send('Failed to parse the Python script output');
    }
  });
});

app.get("/api/functions", async (req, res) => {
  const dir = req.query.directory;

  // Validate the 'directory' parameter
  if (!dir) {
    return res.status(400).send("Directory parameter is required");
  }

  try {
    // Spawn the Python process and wait for it to finish
    const { stdout, stderr } = await new Promise((resolve, reject) => {
      const pythonProcess = spawn("python3", [parseScriptPath, dir, "--type", "functions"]);

      let result = '';
      pythonProcess.stdout.on('data', (data) => {
        result += data.toString();
      });

      pythonProcess.stderr.on('data', (data) => {
        console.error(`Python error: ${data}`);
      });

      pythonProcess.on('close', async (code) => {
        if (code !== 0) {
          return reject(new Error(`Python script exited with code ${code}`));
        }
        resolve({ stdout: result });
      });
    });

    // Parse and send the result
    try {
      const parsedResult = JSON.parse(stdout.replace(/'/g, "\""));
      res.status(200).json(parsedResult);
    } catch (e) {
      console.error(`Error parsing JSON: ${e}`);
      res.status(500).send('Failed to parse the Python script output');
    }

  } catch (e) {
    console.error(`Error executing Python script: ${e}`);
    res.status(500).send(`Failed to execute Python script: ${e.message}`);
  }
});

// Start the server
app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
});
