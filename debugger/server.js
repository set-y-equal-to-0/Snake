const express = require('express')
const app = express()
const bodyParser = require('body-parser')
const http = require('http')
const fetch = require('node-fetch')

const URL = "http://0.0.0.0:8002"

app.use(express.static('./content'))
app.use(bodyParser.json())

app.get('/', function(req, res) {
    const html = path.resolve('content/index.html')
    res.sendFile(html)
})

app.get('/start', function(req, res) {
    let template = {
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
          "food": [],
          "hazards": [],
          "snakes": []
        },
        "you": {}
      }

    fetch(URL + '/start', {
        method: "post",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(template)
    })

    res.setHeader('content-type', 'application/json');
    res.write(JSON.stringify({'status':'200'}));
    res.send();
})

app.post('/move', function(req, res) {
    let template = {
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
          "food": [],
          "hazards": [],
          "snakes": []
        },
        "you": {}
      }

    for (let i = 0; i < req.body["f"].length; i++) {
        template["board"]["food"].push(req.body["f"][i])
    }

    for (let i = 0; i < req.body["h"].length; i++) {
        template["board"]["hazards"].push(req.body["h"][i])
    }

    let you = {
        "id": "you",
        "health": 100,
        "body": [],
        "head": {"x": 0, "y": 0},
        "length": 0
    }

    you["head"] = req.body["yh"][0]
    you["body"].push(you["head"])
    for (let i = 0; i < req.body["yb"].length; i++) {
        you["body"].push(req.body["yb"][i])
    }
    you["length"] = you["body"].length
    template["you"] = you
    template["board"]["snakes"].push(you)
    
    if (req.body["eh"].length > 0) {
        let enemy = {
            "id": "enemy",
            "health": 100,
            "body": [],
            "head": {"x": 0, "y": 0},
            "length": 0
        }
    
        enemy["head"] = req.body["eh"][0]
        enemy["body"].push(enemy["head"])
        for (let i = 0; i < req.body["eb"].length; i++) {
            enemy["body"].push(req.body["eb"][i])
        }
        enemy["length"] = enemy["body"].length
        template["board"]["snakes"].push(enemy)
    }

    fetch(URL + '/move', {
        method: "post",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(template)
    }).then(r => {
        r.json().then(data => {
            res.setHeader('content-type', 'application/json');
            res.write(JSON.stringify(data));
            res.send();
        })
    })
})

const httpServer = http.createServer(app)
httpServer.listen(8000, "0.0.0.0")