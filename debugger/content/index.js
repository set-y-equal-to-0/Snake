
let grid = []
function start() {
    let table = document.getElementById('grid')
    for (let i = 0; i < 11; i++) {
        let row = []
        let tableRow = document.createElement('tr')
        tableRow.className = i.toString()

        for (let j = 0; j < 11; j++) {
            let input = document.createElement('input')
            input.size = 1

            let space = document.createElement('td')
            space.className = j.toString()
            space.appendChild(input)

            tableRow.appendChild(space)
            row.push(input)
        }

        table.prepend(tableRow)
        grid.push(row)
    }
}

start()

function convertGrid() {
    info = {"f": [], "h": [], "eh": [], "eb": [], "yb": [], "yh": []}

    for (let i = 0; i < grid.length; i++) {
        for (let j = 0; j < grid[i].length; j++) {
            for (let k in info) {
                if (grid[i][j].value.toLowerCase() == k) {
                    info[k].push({"x": j, "y": i})
                }
            }
        }
    }

    fetch('/move', {
    method: "post",
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
        },
        body: JSON.stringify(info)
    }).then(res => {
        res.json().then(move => {
            window.alert(move["move"])
        })
    })
}

function startGame() {
    fetch('/start')
}