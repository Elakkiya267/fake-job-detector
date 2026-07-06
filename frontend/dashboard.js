// ── Dashboard JS ─────────────────────────────────────────────────────────────

function getHistory() {
    return JSON.parse(localStorage.getItem('jobGuardHistory') || '[]');
}

// ── Stats ─────────────────────────────────────────────────────────────────────
function updateStats() {
    const history = getHistory();
    const total  = history.length;
    const legit  = history.filter(d => !d.is_fake).length;
    const fake   = history.filter(d => d.is_fake).length;
    const avg    = total > 0
        ? Math.round(history.reduce((s, d) => s + d.score, 0) / total)
        : null;

    document.getElementById('totalScans').textContent      = total;
    document.getElementById('legitimateCount').textContent = legit;
    document.getElementById('fakeCount').textContent       = fake;
    document.getElementById('avgScore').textContent        = avg !== null ? avg : '—';
}

// ── Donut chart ───────────────────────────────────────────────────────────────
function renderChart() {
    const history = getHistory();
    const legit = history.filter(d => !d.is_fake).length;
    const fake  = history.filter(d => d.is_fake).length;

    const empty   = document.getElementById('chartEmpty');
    const wrap    = document.getElementById('chartWrap');

    if (history.length === 0) {
        empty.style.display = 'flex';
        wrap.style.display  = 'none';
        return;
    }

    empty.style.display = 'none';
    wrap.style.display  = 'block';

    const ctx = document.getElementById('ratioChart').getContext('2d');
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Legitimate', 'Fake'],
            datasets: [{
                data: [legit, fake],
                backgroundColor: ['rgba(104,211,145,0.8)', 'rgba(252,129,129,0.8)'],
                borderColor:     ['#68d391', '#fc8181'],
                borderWidth: 2,
                hoverOffset: 6
            }]
        },
        options: {
            responsive: true,
            cutout: '65%',
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#a0aec0',
                        font: { size: 12 },
                        padding: 16
                    }
                },
                tooltip: {
                    callbacks: {
                        label: (ctx) => {
                            const total = ctx.dataset.data.reduce((a, b) => a + b, 0);
                            const pct   = total > 0 ? Math.round((ctx.raw / total) * 100) : 0;
                            return ` ${ctx.label}: ${ctx.raw} (${pct}%)`;
                        }
                    }
                }
            }
        }
    });
}

// ── History table ─────────────────────────────────────────────────────────────
function renderHistory() {
    const history = getHistory();
    const container = document.getElementById('historyContent');

    if (history.length === 0) {
        container.innerHTML = `
            <div class="empty-dash">
                <div class="empty-icon">📋</div>
                <p>No analyses yet. Start scanning job postings!</p>
                <a href="index.html" class="btn btn-primary">Analyze a Job Posting</a>
            </div>`;
        return;
    }

    const rows = history.slice(0, 15).map(d => {
        const badge = d.is_fake
            ? `<span class="badge fake">⚠️ Fake</span>`
            : `<span class="badge legit">✅ Legit</span>`;

        const score = d.score;
        const cls   = score >= 60 ? 'high' : score >= 45 ? 'mid' : 'low';
        const scorePill = `<span class="score-pill ${cls}">${score}</span>`;

        const time = getTimeAgo(new Date(d.timestamp));

        return `<tr>
            <td>${badge}</td>
            <td>${scorePill} / 100</td>
            <td>${d.confidence || '—'}</td>
            <td class="time-lbl">${time}</td>
        </tr>`;
    }).join('');

    container.innerHTML = `
        <table class="history-table">
            <thead>
                <tr>
                    <th>Result</th>
                    <th>Score</th>
                    <th>Confidence</th>
                    <th>Time</th>
                </tr>
            </thead>
            <tbody>${rows}</tbody>
        </table>`;
}

// ── Time helper ───────────────────────────────────────────────────────────────
function getTimeAgo(date) {
    const diff = Date.now() - date.getTime();
    const mins  = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days  = Math.floor(diff / 86400000);

    if (mins  < 1)  return 'Just now';
    if (mins  < 60) return `${mins}m ago`;
    if (hours < 24) return `${hours}h ago`;
    return `${days}d ago`;
}

// ── Clear history ─────────────────────────────────────────────────────────────
function clearHistory() {
    if (confirm('Clear all detection history? This cannot be undone.')) {
        localStorage.removeItem('jobGuardHistory');
        location.reload();
    }
}

// ── Init ──────────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    updateStats();
    renderChart();
    renderHistory();

    const clearBtn = document.getElementById('clearHistoryBtn');
    if (clearBtn) clearBtn.addEventListener('click', clearHistory);
});