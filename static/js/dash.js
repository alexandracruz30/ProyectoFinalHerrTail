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
                    borderColor: '#183b6b', // Primary color
                    backgroundColor: 'rgba(24, 59, 107, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#183b6b',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 6,
                    pointHoverRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(24, 59, 107, 0.9)',
                        titleColor: '#ffffff',
                        bodyColor: '#ffffff',
                        borderColor: '#183b6b',
                        borderWidth: 1,
                        cornerRadius: 8
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Pérdida',
                            color: '#374151'
                        },
                        grid: {
                            color: 'rgba(156, 163, 175, 0.3)'
                        },
                        ticks: {
                            color: '#6b7280'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Época',
                            color: '#374151'
                        },
                        grid: {
                            color: 'rgba(156, 163, 175, 0.3)'
                        },
                        ticks: {
                            color: '#6b7280'
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
                        '#00c37e', // success
                        '#183b6b', // primary
                        '#1b325f'  // secondary
                    ],
                    borderColor: [
                        '#00c37e',
                        '#183b6b',
                        '#1b325f'
                    ],
                    borderWidth: 2,
                    borderRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(17, 24, 39, 0.9)',
                        titleColor: '#ffffff',
                        bodyColor: '#ffffff',
                        borderColor: '#374151',
                        borderWidth: 1,
                        cornerRadius: 8,
                        callbacks: {
                            label: function(context) {
                                return `${context.label}: ${(context.parsed.y * 100).toFixed(1)}%`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 1,
                        title: {
                            display: true,
                            text: 'Valor (%)',
                            color: '#374151'
                        },
                        grid: {
                            color: 'rgba(156, 163, 175, 0.3)'
                        },
                        ticks: {
                            color: '#6b7280',
                            callback: function(value) {
                                return (value * 100).toFixed(0) + '%';
                            }
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            color: '#374151',
                            font: { weight: 'bold' }
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
                        '#183b6b', // primary
                        '#1b325f', // secondary
                        '#e97228', // accent
                        '#ba3259', // pink
                        '#00c37e', // success
                        '#7b8497', // gray-500
                        '#25396e', // gray-600
                        '#bfc8d3', // gray-400
                        '#d1e1ff'  // gray-300
                    ],
                    borderWidth: 3,
                    borderColor: '#ffffff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 15,
                            usePointStyle: true,
                            font: {
                                size: 12
                            },
                            color: '#374151'
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(17, 24, 39, 0.9)',
                        titleColor: '#ffffff',
                        bodyColor: '#ffffff',
                        borderColor: '#374151',
                        borderWidth: 1,
                        cornerRadius: 8,
                        callbacks: {
                            label: function(context) {
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((context.parsed / total) * 100).toFixed(1);
                                return `${context.label}: ${context.parsed} muestras (${percentage}%)`;
                            }
                        }
                    }
                },
                cutout: '60%'
            }
        });

        // Poblar tabla de clasificación
        const classTable = document.getElementById('classTable');
        classificationData.forEach((item, index) => {
            const row = document.createElement('tr');
            const statusIcon = item.f1 >= 0.99 ? '🟢' : item.f1 >= 0.95 ? '🟡' : '🔴';
            
            // Alternar colores de fila para mejor legibilidad
            const rowBg = index % 2 === 0 ? 'bg-white dark:bg-gray-800' : 'bg-gray-50 dark:bg-gray-700';
            row.className = `${rowBg} hover:bg-blue-50 dark:hover:bg-gray-600 transition-colors duration-200`;
            
            row.innerHTML = `
                <td class="px-4 py-3"><strong class="text-gray-900 dark:text-white">${item.class}</strong></td>
                <td class="px-4 py-3 text-center font-semibold ${item.precision >= 0.99 ? 'text-green-600 dark:text-green-400' : item.precision >= 0.95 ? 'text-yellow-600 dark:text-yellow-400' : 'text-red-600 dark:text-red-400'}">${item.precision.toFixed(2)}</td>
                <td class="px-4 py-3 text-center font-semibold ${item.recall >= 0.99 ? 'text-green-600 dark:text-green-400' : item.recall >= 0.95 ? 'text-yellow-600 dark:text-yellow-400' : 'text-red-600 dark:text-red-400'}">${item.recall.toFixed(2)}</td>
                <td class="px-4 py-3 text-center font-semibold ${item.f1 >= 0.99 ? 'text-green-600 dark:text-green-400' : item.f1 >= 0.95 ? 'text-yellow-600 dark:text-yellow-400' : 'text-red-600 dark:text-red-400'}">${item.f1.toFixed(2)}</td>
                <td class="px-4 py-3 text-center font-semibold text-gray-700 dark:text-gray-300">${item.support}</td>
                <td class="px-4 py-3 text-center text-xl">${statusIcon}</td>
            `;
            classTable.appendChild(row);
        });

        // Poblar matriz de confusión con diagonal resaltada
        const confusionMatrixTable = document.getElementById('confusionMatrix');
        confusionMatrix.forEach((row, rowIndex) => {
            const tr = document.createElement('tr');
            
            // Alternar colores de fila
            const rowBg = rowIndex % 2 === 0 ? 'bg-white dark:bg-gray-800' : 'bg-gray-50 dark:bg-gray-700';
            tr.className = `${rowBg} hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors duration-200`;
            
            row.forEach((cell, cellIndex) => {
                const td = document.createElement('td');
                td.textContent = cell;
                td.className = 'px-3 py-3 text-center font-semibold text-sm text-gray-700 dark:text-gray-300';
                
                if (cellIndex === 0) {
                    // Primera columna (etiquetas de fila)
                    td.className = 'px-3 py-3 text-left text-gray-800 dark:text-gray-200 font-bold';
                } else if (typeof cell === 'number' && cell >= 600) {
                    // Resaltar números grandes (600 o más) con fondo azul
                    td.className = 'px-3 py-3 text-center font-bold text-lg bg-blue-100 dark:bg-blue-800 text-blue-800 dark:text-blue-100 border border-blue-200 dark:border-blue-600';
                }
                
                tr.appendChild(td);
            });
            confusionMatrixTable.appendChild(tr);
        });