const express = require('express');
const path = require('path');
const { spawn } = require('child_process');
const { promisify } = require('util');
const fs = require('fs');


const app = express();
const parseScriptPath = path.join(__dirname, "parse.py");
const port = 3000;


const executePythonScript = (dir, type) => {
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn('python3', [parseScriptPath, dir, '--type', type]);

    let result = '';

    // Collect data from stdout
    pythonProcess.stdout.on('data', (data) => {
      result += data.toString();
    });

    // Handle errors from stderr
    pythonProcess.stderr.on('data', (data) => {
      console.error(`Python error: ${data}`);
    });

    // Wait for the process to exit
    pythonProcess.on('close', async (code) => {
      if (code !== 0) {
        return reject(new Error(`Python script exited with code ${code}`));
      }
      await new Promise(resolve => setTimeout(resolve, 1000));
      console.log(result)
      resolve(result);
    });

    // Handle errors in case the process is not spawned correctly
    pythonProcess.on('error', (err) => {
      reject(err);
    });
  });
};

// Serve static files from the 'public' directory
app.use(express.static(path.join(__dirname, 'public')));

app.get("/api/:type", async (req, res) => {
  const { type } = req.params;
  const dir = req.query.directory;

  // Validate the 'directory' parameter
  if (!dir) {
    return res.status(400).send("Directory parameter is required");
  }

  try {
    const stdout = await executePythonScript(dir, type);
    fs.readFile("./graph.json", 'utf8', (err, data) => {
      if (err) {
        console.error('Error reading file:', err);
        res.status(500).send('Failed to parse the Python script output');
        return;
      }

      try {
        // Parse the JSON data
        const jsonData = JSON.parse(data);

        res.status(200).json(jsonData);
        return;
      } catch (parseError) {
        console.error('Error parsing JSON:', parseError);
        res.status(500).send('Failed to parse the Python script output');
        return;
      }
    });

    //const parsedResult = JSON.parse(stdout.replace(/'/g, "\""));
  } catch (e) {
    console.error(`Error parsing JSON: ${e}`);
    res.status(500).send('Failed to parse the Python script output');
  }
});

// Start the server
app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
});
