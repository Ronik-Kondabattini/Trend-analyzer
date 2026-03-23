/**
 * static/js/dashboard.js — Dashboard controller.
 *
 * Pure vanilla JS. No React, no Vue, no jQuery.
 * Fetches data from Django API views via AJAX (using api.js).
 * Initial data is server-rendered by Django template into window.INIT_DATA.
 */

const EMOJI_MAP = {technology:'💻',fitness:'💪',cooking:'🍳',finance:'💰',gaming:'🎮',travel:'✈️',education:'📚',default:'🔍'};

function scoreClass(s) { return s>=90?'sc-green':s>=75?'sc-cyan':s>=60?'sc-amber':'sc-red'; }
function scoreBg(s) { return s>=90?'bg-green':s>=75?'bg-cyan':s>=60?'bg-amber':'bg-red'; }
function diffTag(d) { return d==='Easy'?'itag-easy':d==='Medium'?'itag-medium':'itag-hard'; }
function potTag(p) { return p==='Very High'?'itag-vhigh':p==='High'?'itag-high':'itag-med'; }
function esc(s) { const d=document.createElement('div');d.textContent=s;return d.innerHTML; }

const D = {
    data: window.INIT_DATA || {},
    result: null,
    tab: 'videos',
    sidebarTab: 'history',
    savedTitles: new Set(),

    init() {
        // Populate saved titles set
        (this.data.saved||[]).forEach(s => this.savedTitles.add(s.idea_title));
        this.updateBadge();
        this.renderStats();
        this.renderTrending();
        this.bindEvents();
    },

    bindEvents() {
        document.getElementById('search-input').addEventListener('keydown', e => { if(e.key==='Enter') this.analyze(); });
        document.getElementById('search-btn').addEventListener('click', () => this.analyze());
        document.getElementById('btn-history').addEventListener('click', () => this.openSidebar('history'));
        document.getElementById('btn-saved').addEventListener('click', () => this.openSidebar('saved'));
        document.getElementById('sidebar-close').addEventListener('click', () => this.closeSidebar());
        document.getElementById('sidebar-overlay').addEventListener('click', () => this.closeSidebar());
        document.getElementById('stab-history').addEventListener('click', () => this.switchSidebarTab('history'));
        document.getElementById('stab-saved').addEventListener('click', () => this.switchSidebarTab('saved'));
    },

    updateBadge() {
        const b = document.getElementById('saved-badge');
        const n = (this.data.saved||[]).length;
        b.textContent = n;
        b.classList.toggle('show', n > 0);
    },

    renderStats() {
        const s = this.data.stats;
        if (!s || !s.total_searches) { document.getElementById('stats-bar').innerHTML=''; return; }
        if (this.result) { document.getElementById('stats-bar').innerHTML=''; return; }
        document.getElementById('stats-bar').innerHTML = [
            {i:'🔍',v:s.total_searches,l:'Searches'},
            {i:'📊',v:(s.avg_trend_score||0)+'%',l:'Avg Score'},
            {i:'🎯',v:s.top_category,l:'Top Category'},
            {i:'📌',v:s.saved_ideas_count,l:'Saved'},
        ].map(x=>`<div class="stat-card"><span class="si">${x.i}</span><div><div class="sv">${esc(String(x.v))}</div><div class="sl">${x.l}</div></div></div>`).join('');
    },

    renderTrending() {
        const t = this.data.trending || [];
        const el = document.getElementById('home-section');
        if (this.result) { el.classList.add('hidden'); return; }
        el.classList.remove('hidden');
        el.innerHTML = `
            <div class="section-hdr"><span style="font-size:1.25rem">🔥</span><h3>Trending Now</h3><span class="hint">Click to analyze</span></div>
            <div class="trend-grid">${t.map(x=>`
                <button class="trend-card" data-topic="${esc(x.name)}">
                    <div class="trend-top"><span class="trend-emoji">${x.emoji}</span><div class="flex" style="display:flex;align-items:center;gap:4px"><div style="width:6px;height:6px;border-radius:50%" class="${scoreBg(x.trend_score)}"></div><span class="trend-score ${scoreClass(x.trend_score)}">${x.trend_score}%</span></div></div>
                    <div class="trend-name">${esc(x.name)}</div>
                    <div class="trend-cat">${esc(x.category)}</div>
                </button>
            `).join('')}</div>
        `;
        el.querySelectorAll('.trend-card').forEach(btn => {
            btn.addEventListener('click', () => {
                const topic = btn.dataset.topic;
                document.getElementById('search-input').value = topic;
                this.analyze(topic);
            });
        });
    },

    async analyze(topicOverride) {
        const input = document.getElementById('search-input');
        const topic = topicOverride || input.value.trim();
        if (!topic) return;
        input.value = topic;

        // Show loading
        document.getElementById('home-section').classList.add('hidden');
        document.getElementById('results-section').classList.add('hidden');
        document.getElementById('stats-bar').innerHTML = '';
        const ld = document.getElementById('loading-section');
        ld.classList.remove('hidden');
        ld.innerHTML = `<div style="display:flex;flex-direction:column;align-items:center;padding:100px 0">
            <div style="position:relative"><div style="width:80px;height:80px;border-radius:50%;border:3px solid rgba(255,255,255,.04);border-top-color:#8b5cf6;animation:spin .8s linear infinite"></div></div>
            <p style="color:var(--muted);margin-top:2rem;font-size:14px">Analyzing <span style="color:#8b5cf6;font-weight:500">"${esc(topic)}"</span></p>
        </div>`;

        try {
            this.result = await API.analyze(topic);
            // Refresh history & stats
            this.data.history = await API.getHistory();
            this.data.stats = await API.getStats();
            this.renderResults();
        } catch(e) {
            console.error(e);
            ld.innerHTML = `<div class="alert err" style="max-width:400px;margin:100px auto">Analysis failed. Please try again.</div>`;
        }
    },

    renderResults() {
        document.getElementById('loading-section').classList.add('hidden');
        document.getElementById('home-section').classList.add('hidden');
        const el = document.getElementById('results-section');
        el.classList.remove('hidden');
        const r = this.result;

        // Metrics
        const metrics = [
            {l:'Trend Score',v:r.trend_score+'%',g:'from-violet',b:r.trend_score,gc:'linear-gradient(90deg,#8b5cf6,#c026d3)'},
            {l:'Volume',v:Math.round(r.search_volume/1000)+'K',g:'from-cyan',b:Math.min(r.search_volume/5000,100),gc:'linear-gradient(90deg,#06b6d4,#3b82f6)'},
            {l:'Competition',v:r.competition,g:'from-amber',b:r.competition==='Low'?30:r.competition==='Medium'?60:90,gc:'linear-gradient(90deg,#f59e0b,#f97316)'},
            {l:'Growth',v:'+'+r.growth_percentage+'%',g:'from-green',b:Math.min(r.growth_percentage/2,100),gc:'linear-gradient(90deg,#10b981,#22c55e)'},
        ];

        el.innerHTML = `
            <div class="metrics">${metrics.map(m=>`
                <div class="metric"><div class="ml">${m.l}</div><div class="mv">${m.v}</div>
                <div class="bar-track"><div class="bar-fill" style="width:${m.b}%;background:${m.gc}"></div></div></div>
            `).join('')}</div>

            <div class="topic-hdr">
                <span class="topic-emoji">${EMOJI_MAP[r.category]||'🔍'}</span>
                <div><div class="topic-name">${esc(r.topic)}</div><div class="topic-meta">${esc(r.category)} • ${r.videos.length} videos • ${r.content_ideas.length} ideas</div></div>
                <div class="related">${r.related_topics.map(t=>`<button class="related-tag" data-topic="${esc(t)}">#${esc(t)}</button>`).join('')}</div>
            </div>

            <div class="tabs">
                <button class="tab ${this.tab==='videos'?'active':''}" data-tab="videos">▶ Videos</button>
                <button class="tab ${this.tab==='ideas'?'active':''}" data-tab="ideas">💡 Ideas</button>
            </div>

            <div id="tab-content"></div>

            <div style="text-align:center"><button class="back-btn" id="back-btn">← Analyze another topic</button></div>
        `;

        // Bind
        el.querySelectorAll('.related-tag').forEach(b => b.addEventListener('click', () => {
            document.getElementById('search-input').value = b.dataset.topic;
            this.analyze(b.dataset.topic);
        }));
        el.querySelectorAll('.tab').forEach(b => b.addEventListener('click', () => {
            this.tab = b.dataset.tab;
            el.querySelectorAll('.tab').forEach(t=>t.classList.toggle('active',t.dataset.tab===this.tab));
            this.renderTab();
        }));
        document.getElementById('back-btn').addEventListener('click', () => this.goHome());
        this.renderTab();
    },

    renderTab() {
        const c = document.getElementById('tab-content');
        if (this.tab === 'videos') this.renderVideos(c);
        else this.renderIdeas(c);
    },

    renderVideos(container) {
        const r = this.result;
        container.innerHTML = `<div class="vid-list">${r.videos.map(v => {
            const g = 'g-'+(v.thumbnail||'default');
            return `<a href="${esc(v.youtube_url)}" target="_blank" rel="noopener" class="vid-card">
                <div class="vid-thumb"><div class="vid-thumb-bg ${g}"></div><div class="vid-overlay"></div>
                    <div class="vid-play"><svg width="20" height="20" fill="white" viewBox="0 0 24 24"><polygon points="5 3 19 12 5 21"/></svg></div>
                    <div class="vid-dur">${esc(v.duration)}</div>
                    <div class="vid-yt"><svg viewBox="0 0 24 24"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814z" fill="#FF0000"/><path d="M9.545 15.568V8.432L15.818 12l-6.273 3.568z" fill="white"/></svg><span>YouTube</span></div>
                </div>
                <div class="vid-info">
                    <div class="vid-title line-clamp-2">${esc(v.title)}</div>
                    <div class="vid-channel">${esc(v.channel)}</div>
                    <div class="vid-stats"><span>👁 ${esc(v.views)}</span><span>⏱ ${esc(v.duration)}</span><span class="vs-score ${scoreClass(v.trend_score)}">⭐ ${v.trend_score}%</span></div>
                </div>
            </a>`;
        }).join('')}</div>`;
    },

    renderIdeas(container) {
        const r = this.result;
        container.innerHTML = `<div class="idea-grid">${r.content_ideas.map((idea, i) => {
            const saved = this.savedTitles.has(idea.title);
            return `<div class="idea-card">
                <div class="idea-top"><span class="idea-icon">${idea.icon}</span>
                    <button class="idea-save ${saved?'saved':''}" data-idx="${i}" ${saved?'disabled':''}>${saved?'✓':'+'}</button>
                </div>
                <div class="idea-type">${esc(idea.type)}</div>
                <div class="idea-title">${esc(idea.title)}</div>
                <div class="idea-tags">
                    <span class="itag ${diffTag(idea.difficulty)}">${esc(idea.difficulty)}</span>
                    <span class="itag ${potTag(idea.potential)}">${esc(idea.potential)}</span>
                </div>
            </div>`;
        }).join('')}</div>`;
        container.querySelectorAll('.idea-save:not(.saved)').forEach(btn => {
            btn.addEventListener('click', async () => {
                const idea = r.content_ideas[parseInt(btn.dataset.idx)];
                try {
                    await API.saveIdea({topic:r.topic, idea_type:idea.type, idea_title:idea.title, difficulty:idea.difficulty, potential:idea.potential});
                    this.savedTitles.add(idea.title);
                    this.data.saved = await API.getSaved();
                    this.updateBadge();
                    btn.textContent = '✓';
                    btn.classList.add('saved');
                    btn.disabled = true;
                } catch(e) { console.error(e); }
            });
        });
    },

    goHome() {
        this.result = null;
        this.tab = 'videos';
        document.getElementById('search-input').value = '';
        document.getElementById('results-section').classList.add('hidden');
        document.getElementById('loading-section').classList.add('hidden');
        this.renderStats();
        this.renderTrending();
    },

    // ---- Sidebar ----
    openSidebar(tab) {
        document.getElementById('sidebar-overlay').classList.remove('hidden');
        document.getElementById('sidebar-panel').classList.remove('hidden');
        this.switchSidebarTab(tab);
    },
    closeSidebar() {
        document.getElementById('sidebar-overlay').classList.add('hidden');
        document.getElementById('sidebar-panel').classList.add('hidden');
    },
    switchSidebarTab(tab) {
        this.sidebarTab = tab;
        document.getElementById('stab-history').classList.toggle('active', tab==='history');
        document.getElementById('stab-saved').classList.toggle('active', tab==='saved');
        if (tab==='history') this.renderSidebarHistory();
        else this.renderSidebarSaved();
    },

    renderSidebarHistory() {
        const c = document.getElementById('sidebar-content');
        const h = this.data.history || [];
        if (!h.length) { c.innerHTML='<div class="sb-empty">No searches yet</div>'; return; }
        c.innerHTML = h.map(x => `
            <div class="sh-card">
                <span class="sh-emoji">${EMOJI_MAP[x.category]||'🔍'}</span>
                <div class="sh-body">
                    <button class="sh-topic" data-topic="${esc(x.topic)}">${esc(x.topic)}</button>
                    <div class="sh-meta"><span class="${scoreClass(x.trend_score)}">${x.trend_score}%</span> • ${new Date(x.created_at).toLocaleDateString()}</div>
                </div>
                <button class="sh-del" data-id="${x.id}">🗑</button>
            </div>
        `).join('');
        c.querySelectorAll('.sh-topic').forEach(b => b.addEventListener('click', () => {
            this.closeSidebar();
            document.getElementById('search-input').value = b.dataset.topic;
            this.analyze(b.dataset.topic);
        }));
        c.querySelectorAll('.sh-del').forEach(b => b.addEventListener('click', async () => {
            await API.delHistory(parseInt(b.dataset.id));
            this.data.history = await API.getHistory();
            this.data.stats = await API.getStats();
            this.renderSidebarHistory();
            if (!this.result) this.renderStats();
        }));
    },

    renderSidebarSaved() {
        const c = document.getElementById('sidebar-content');
        const s = this.data.saved || [];
        if (!s.length) { c.innerHTML='<div class="sb-empty">No saved ideas yet</div>'; return; }
        c.innerHTML = s.map(x => `
            <div class="si-card">
                <div class="si-top"><span class="si-type">${esc(x.idea_type)}</span><button class="si-del" data-id="${x.id}">🗑</button></div>
                <div class="si-title">${esc(x.idea_title)}</div>
                <div class="si-meta"><span class="chip">${esc(x.topic)}</span><span>${esc(x.difficulty)} • ${esc(x.potential)}</span></div>
            </div>
        `).join('');
        c.querySelectorAll('.si-del').forEach(b => b.addEventListener('click', async () => {
            await API.delSaved(parseInt(b.dataset.id));
            this.data.saved = await API.getSaved();
            this.savedTitles = new Set(this.data.saved.map(x=>x.idea_title));
            this.updateBadge();
            this.renderSidebarSaved();
        }));
    },
};

document.addEventListener('DOMContentLoaded', () => D.init());
