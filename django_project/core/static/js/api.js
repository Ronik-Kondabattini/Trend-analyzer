/**
 * static/js/api.js — AJAX client with Django CSRF protection.
 *
 * All backend calls go through this. Uses Django session cookies.
 * CSRF token is read from the 'csrftoken' cookie set by Django.
 */
window.API = {
    _csrf() {
        const m = document.cookie.match(/csrftoken=([^;]+)/);
        return m ? m[1] : '';
    },

    async _req(url, method, body) {
        const opts = {
            method,
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': this._csrf() },
            credentials: 'same-origin',
        };
        if (body) opts.body = JSON.stringify(body);
        const r = await fetch(url, opts);
        const d = await r.json();
        if (!r.ok) throw { status: r.status, ...d };
        return d;
    },

    analyze(topic)    { return this._req('/api/analyze/', 'POST', { topic }); },
    getHistory()      { return this._req('/api/history/', 'GET'); },
    delHistory(id)    { return this._req('/api/history/', 'DELETE', { id }); },
    getSaved()        { return this._req('/api/saved-ideas/', 'GET'); },
    saveIdea(data)    { return this._req('/api/saved-ideas/', 'POST', data); },
    delSaved(id)      { return this._req('/api/saved-ideas/', 'DELETE', { id }); },
    getTrending()     { return this._req('/api/trending/', 'GET'); },
    getStats()        { return this._req('/api/stats/', 'GET'); },
};
