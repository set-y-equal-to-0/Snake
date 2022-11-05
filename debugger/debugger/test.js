const fetch = require('node-fetch');

fetch('http://127.0.0.1:8002/start', {
  method: "post",
  headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      "game": {
        "id": "totally-unique-game-id",
        "ruleset": {
          "name": "standard",
          "version": "v1.2.3"
        },
        "map": "standard",
        "timeout": 500,
        "source": "league"
      },
      "turn": 0,
      "board": {
        "height": 11,
        "width": 11,
        "food": [
          {"x": 9, "y": 5}
        ],
        "hazards": [
          {"x": 2, "y": 2},
          {"x": 2, "y": 3},
          {"x": 2, "y": 4},
          {"x": 2, "y": 5},
          {"x": 2, "y": 6},
          {"x": 2, "y": 7},
          {"x": 2, "y": 8},
          {"x": 2, "y": 9},
          {"x": 2, "y": 10},
        ],
        "snakes": [
          {
            "health": 100,
            "body": [
              {"x": 0, "y": 10}, 
              {"x": 0, "y": 9}
            ],
            "head": {"x": 0, "y": 10},
            "length": 2,
            "squad": "2",
          }
        ]
      },
      "you": {
        "health": 100,
        "body": [
          {"x": 2, "y": 1}, 
          {"x": 2, "y": 0}
        ],
        "head": {"x": 2, "y": 1},
        "length": 2,
        "squad": "1"
      }
    })
})


fetch('http://127.0.0.1:8002/move', {
  method: "post",
  headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      "game": {
        "id": "totally-unique-game-id",
        "ruleset": {
          "name": "standard",
          "version": "v1.2.3"
        },
        "map": "standard",
        "timeout": 500,
        "source": "league"
      },
      "turn": 0,
      "board": {
        "height": 11,
        "width": 11,
        "food": [
          {"x": 2, "y": 10}
        ],
        "hazards": [
        ],
        "snakes": [
          {
            "health": 100,
            "body": [
              {"x": 3, "y": 10}, 
              {"x": 4, "y": 10}
            ],
            "head": {"x": 3, "y": 10},
            "length": 2,
            "squad": "2",
          },{
            "health": 100,
            "body": [
              {"x": 2, "y": 9}, 
              {"x": 2, "y": 8}
            ],
            "head": {"x": 2, "y": 9},
            "length": 2,
            "squad": "1"
          }
        ]
      },
      "you": {
        "health": 100,
        "body": [
          {"x": 2, "y": 9}, 
          {"x": 2, "y": 8}
        ],
        "head": {"x": 2, "y": 9},
        "length": 2,
        "squad": "1"
      }
    })
})