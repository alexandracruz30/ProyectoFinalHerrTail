// Datos
        const trainingData = {
            epochs: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
            loss: [0.1630, 0.0960, 0.0876, 0.0787, 0.0699, 0.0612, 0.0549, 0.0500, 0.0454, 0.0406, 0.0360, 0.0319, 0.0285, 0.0257, 0.0234]
        };

        const classificationData = [
            { class: 'Center', precision: 0.99, recall: 1.00, f1: 0.99, support: 721 },
            { class: 'Donut', precision: 1.00, recall: 1.00, f1: 1.00, support: 671 },
            { class: 'Edge-Loc', precision: 0.99, recall: 0.97, f1: 0.98, support: 765 },
            { class: 'Edge-Ring', precision: 0.99, recall: 1.00, f1: 1.00, support: 667 },
            { class: 'Loc', precision: 0.99, recall: 0.98, f1: 0.98, support: 793 },
            { class: 'Near-full', precision: 1.00, recall: 1.00, f1: 1.00, support: 699 },
            { class: 'Random', precision: 1.00, recall: 1.00, f1: 1.00, support: 693 },
            { class: 'Scratch', precision: 1.00, recall: 0.97, f1: 0.99, support: 676 },
            { class: 'None', precision: 0.95, recall: 0.99, f1: 0.97, support: 819 }
        ];

        const confusionMatrix = [
            ['Center', 718, 0, 0, 0, 1, 0, 0, 0, 1],
            ['Donut', 0, 671, 0, 0, 0, 0, 0, 0, 0],
            ['Edge-Loc', 0, 0, 740, 4, 3, 0, 0, 0, 18],
            ['Edge-Ring', 0, 0, 2, 665, 0, 0, 0, 0, 0],
            ['Loc', 5, 0, 2, 0, 774, 0, 0, 1, 11],
            ['Near-full', 0, 0, 0, 0, 0, 697, 2, 0, 0],
            ['Random', 0, 0, 1, 0, 0, 0, 692, 0, 0],
            ['Scratch', 0, 0, 0, 0, 0, 0, 0, 659, 17],
            ['None', 1, 0, 2, 0, 4, 0, 0, 0, 812]
        ];

        // Gráfico de pérdida
        const lossCtx = document.getElementById('lossChart').getContext('2d');
        new Chart(lossCtx, {
            type: 'line',
            data: {
                labels: trainingData.epochs,
                datasets: [{
                    label: 'Pérdida',
                    data: trainingData.loss,
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#667eea',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Pérdida'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Época'
                        }
                    }
                }
            }
        });

        // Gráfico de métricas
        const metricsCtx = document.getElementById('metricsChart').getContext('2d');
        new Chart(metricsCtx, {
            type: 'bar',
            data: {
                labels: ['Precisión', 'Recall', 'F1-Score'],
                datasets: [{
                    label: 'Métricas',
                    data: [0.996, 0.99, 0.99],
                    backgroundColor: [
                        'rgba(255, 107, 107, 0.8)',
                        'rgba(102, 126, 234, 0.8)',
                        'rgba(118, 75, 162, 0.8)'
                    ],
                    borderColor: [
                        '#ff6b6b',
                        '#667eea',
                        '#764ba2'
                    ],
                    borderWidth: 2,
                    borderRadius: 10
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 1,
                        title: {
                            display: true,
                            text: 'Valor'
                        }
                    }
                }
            }
        });

        // Gráfico de distribución
        const distributionCtx = document.getElementById('distributionChart').getContext('2d');
        new Chart(distributionCtx, {
            type: 'doughnut',
            data: {
                labels: classificationData.map(item => item.class),
                datasets: [{
                    data: classificationData.map(item => item.support),
                    backgroundColor: [
                        '#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#ffeaa7',
                        '#dda0dd', '#98d8c8', '#f7dc6f', '#bb8fce'
                    ],
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });

        // Poblar tabla de clasificación
        const classTable = document.getElementById('classTable');
        classificationData.forEach(item => {
            const row = document.createElement('tr');
            row.className = 'border-b hover:bg-gray-50';
            
            const statusText = item.f1 >= 0.99 ? 'Excelente' : item.f1 >= 0.95 ? 'Bueno' : 'Mejorar';
            const statusClass = item.f1 >= 0.99 ? 'bg-green-100 text-green-800' : 
                               item.f1 >= 0.95 ? 'bg-yellow-100 text-yellow-800' : 
                               'bg-red-100 text-red-800';
            
            row.innerHTML = `
                <td class="py-1 px-2 font-medium text-blue-900">${item.class}</td>
                <td class="py-1 px-2 text-center">${(item.precision * 100).toFixed(0)}%</td>
                <td class="py-1 px-2 text-center">${(item.recall * 100).toFixed(0)}%</td>
                <td class="py-1 px-2 text-center">${(item.f1 * 100).toFixed(0)}%</td>
                <td class="py-1 px-2 text-center">${item.support}</td>
                <td class="py-1 px-2 text-center">
                    <span class="px-2 py-1 text-xs rounded-full ${statusClass}">
                        ${statusText}
                    </span>
                </td>
            `;
            classTable.appendChild(row);
        });

        // Poblar matriz de confusión
        const confusionMatrixTable = document.getElementById('confusionMatrix');
        confusionMatrix.forEach((row, rowIndex) => {
            const tr = document.createElement('tr');
            tr.className = 'border-b hover:bg-gray-50';
            
            row.forEach((cell, cellIndex) => {
                const td = document.createElement('td');
                td.textContent = cell;
                
                if (cellIndex === 0) {
                    // Primera columna (nombres de clases)
                    td.className = 'py-1 px-2 font-medium text-blue-900 bg-gray-50';
                } else if (cellIndex === rowIndex && rowIndex > 0) {
                    // Diagonal principal (predicciones correctas)
                    td.className = 'py-1 px-2 diagonal';
                } else {
                    // Celdas normales
                    td.className = 'py-1 px-2 text-center';
                    if (cellIndex > 0 && cell > 0 && cellIndex !== rowIndex) {
                        // Errores de clasificación en rojo suave
                        td.style.backgroundColor = '#fef2f2';
                        td.style.color = '#dc2626';
                    }
                }
                
                tr.appendChild(td);
            });
            confusionMatrixTable.appendChild(tr);
        });
