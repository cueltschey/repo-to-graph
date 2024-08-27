# Repo to graph
This is a python tool for parsing a codebase and generating a traversable graph to help visualize file relationships.

To load your codebase as json:
```
git clone https://github.com/cueltschey/repo-to-graph
cd repo-to-graph
python3 ./parse.py <root dir of your codebase> --output ./public/graph.json
```

The graph.json is loaded by default by the node server

To start the node server:
```
npm i express
npm run start
```

Then visit http://localhost:3000 to see the graph

This repo was made to help analyze the [Soft T UE Project](https://github.com/oran-testing/soft-t-ue) at Mississippi State University

![zoom.png](https://github.com/cueltschey/repo-to-graph/blob/main/doc/images/zoom.png)
![all.png](https://github.com/cueltschey/repo-to-graph/blob/main/doc/images/all.png)
