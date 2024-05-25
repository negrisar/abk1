function uploadFiles() {
    const lawFile = document.getElementById('lawFile').files[0];
    const contractFile = document.getElementById('contractFile').files[0];

    const lawFormData = new FormData();
    lawFormData.append('lawFile', lawFile);

    const contractFormData = new FormData();
    contractFormData.append('contractFile', contractFile);

    fetch('/upload-law', {
        method: 'POST',
        body: lawFormData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to upload law file');
        }
        return response.json();
    })
    .then(lawData => {
        console.log(lawData);
        fetch('/upload-contract', {
            method: 'POST',
            body: contractFormData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to upload contract file');
            }
            return response.json();
        })
        .then(contractData => {
            console.log(contractData);
            analyzeDocuments(lawData.text, contractData.text);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function analyzeDocuments(lawText, contractText) {
    fetch('/analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ law_text: lawText, contract_text: contractText })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        const resultsDiv = document.getElementById('results');
        resultsDiv.innerHTML = JSON.stringify(data, null, 2);
    });
}