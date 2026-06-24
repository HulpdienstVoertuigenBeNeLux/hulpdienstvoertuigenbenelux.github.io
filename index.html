<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <title>Brandweer Voertuig Statistieken</title>
    <style>
        body { font-family: sans-serif; margin: 20px; }
        table { border-collapse: collapse; width: 100%; max-width: 600px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        #last-update { margin-top: 20px; color: #666; font-size: 0.9em; }
    </style>
</head>
<body>

    <h2>Aantal Brandweervoertuigen per type</h2>
    <table id="vehicle-table">
        <thead>
            <tr>
                <th>Type Voertuig</th>
                <th>Aantal</th>
            </tr>
        </thead>
        <tbody id="table-body"></tbody>
    </table>

    <div id="last-update">Laatste update: Laden...</div>

    <script>
        async function loadData() {
            try {
                // Haal de JSON data op
                const response = await fetch('vehicle_counts.json');
                const data = await response.json();

                const tbody = document.getElementById('table-body');
                
                // Vul de tabel
                for (const [type, count] of Object.entries(data)) {
                    const row = `<tr><td>${type}</td><td>${count}</td></tr>`;
                    tbody.innerHTML += row;
                }

                // Haal de timestamp op van de laatste GitHub commit via de API
                const commitResponse = await fetch('https://api.github.com/repos/JOUW_GEBRUIKERSNAAM/JOUW_REPO_NAAM/commits?path=vehicle_counts.json');
                const commits = await commitResponse.json();
                const date = new Date(commits[0].commit.committer.date);
                document.getElementById('last-update').innerText = "Laatste update: " + date.toLocaleString('nl-NL');
            
            } catch (error) {
                document.getElementById('last-update').innerText = "Fout bij laden van data.";
            }
        }
        loadData();
    </script>
</body>
</html>
