import os

html_head = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PHANTOM V</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;700&family=Share+Tech+Mono&display=swap" rel="stylesheet">
"""

css_content = """
    <style>
        :root {
            --bg-color: #000000;
            --player-color: #ffffff;
            --cyan: #ffffff;      /* Simplified per request */
            --amber: #cccccc;
            --red: #ff0000;
            --purple: #aa00ff;
            --ui-font: 'Inter', sans-serif;
            --title-font: 'Orbitron', sans-serif;
            --mono-font: 'Share Tech Mono', monospace;
            --arena-bg: #000000;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            background-color: var(--bg-color);
            color: #fff;
            font-family: var(--ui-font);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            overflow: hidden;
            user-select: none;
            transition: background-color 2s ease;
        }

        #game-wrapper {
            position: relative;
            width: 800px;
            height: 600px;
            box-shadow: 0 0 1px rgba(255, 255, 255, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.1);
            background: var(--arena-bg);
            overflow: hidden;
        }
        
        #parallax-bg {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            pointer-events: none;
            z-index: 1;
            display: none;
            overflow: hidden;
        }

        canvas {
            display: block;
            position: absolute;
            z-index: 5;
        }

        /* UI Overlays */
        #ui-layer {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            z-index: 10;
            pointer-events: none;
        }

        .screen {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            display: none;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background: rgba(0, 0, 0, 1.0);
            pointer-events: all;
        }
        .screen.active { display: flex; }

        h1, h2, h3 { font-family: var(--title-font); letter-spacing: 2px; }
        
        button {
            padding: 12px 30px;
            margin: 10px;
            background: transparent;
            border: 1px solid rgba(255, 255, 255, 0.5);
            color: #fff;
            font-family: var(--title-font);
            cursor: pointer;
            transition: all 0.2s;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        button:hover {
            background: rgba(255,255,255,1);
            color: #000;
        }
        button:disabled {
            opacity: 0.3;
            cursor: not-allowed;
        }

        /* Main Menu */
        .title-glitch {
            font-size: 64px;
            letter-spacing: 15px;
            margin-bottom: 5px;
        }
        .subtitle {
            font-family: var(--mono-font);
            opacity: 0.6;
            margin-bottom: 40px;
        }
        .player-stats {
            margin-bottom: 30px;
            text-align: center;
            font-family: var(--mono-font);
        }
        .rank-display { font-weight: bold; font-size: 18px; margin-top: 5px;}
        .sp-display { margin-top: 5px;}

        /* Sanctum Menu */
        #sanctum-screen { justify-content: flex-start; padding: 30px; }
        .sanctum-header {
            width: 100%; display: flex; justify-content: space-between; align-items: center;
            margin-bottom: 20px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 15px;
        }
        .tabs { display: flex; gap: 10px; margin-bottom: 20px; }
        .tab-btn { border: none; border-bottom: 2px solid transparent; padding: 10px 20px; }
        .tab-btn.active { border-bottom-color: #fff; background: rgba(255,255,255,0.1); }
        .tab-content { width: 100%; height: 400px; display: none; overflow-y: auto; }
        .tab-content.active { display: flex; flex-direction: column; gap: 10px; }
        
        .item-card {
            display: flex; justify-content: space-between; align-items: center;
            padding: 15px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1);
        }
        .item-card.equipped { border-color: #fff; background: rgba(255,255,255,0.1); }
        .item-info h3 { margin-bottom: 5px; }
        .item-info p { font-family: var(--mono-font); font-size: 12px; opacity: 0.7; }

        /* HUD */
        #hud {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            pointer-events: none; padding: 20px; display: none; z-index: 10;
        }
        .hud-top { display: flex; justify-content: space-between; align-items: flex-start; }
        .hp-container { display: flex; flex-direction: column; width: 200px; display: none;}
        .fighter-name { font-family: var(--title-font); font-size: 16px; margin-bottom: 5px;}
        .hp-bar { width: 100%; height: 8px; background: rgba(255,255,255,0.1); position: relative; border: 1px solid rgba(255,255,255,0.2); }
        .hp-fill { height: 100%; transition: width 0.1s; }
        #player-hp { background: #fff; }
        #phantom-hp { background: var(--red); }
        .fighter-title { font-size: 10px; opacity: 0.6; margin-top: 2px; }

        .center-hud { text-align: center; }
        .round-text { font-family: var(--title-font); font-size: 16px; letter-spacing: 2px; opacity:0.8;}
        
        .corruption-container { position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%); text-align: center; width: 300px; display:none;}
        .corruption-bar { height: 2px; background: rgba(255,0,0,0.2); margin-top: 5px; position:relative; overflow: hidden;}
        #corruption-fill { height: 100%; background: var(--red); width: 0%; transition: width 0.5s;}
        .corr-label { font-size: 10px; letter-spacing: 2px; color: var(--red); opacity: 0.5;}

        /* Rage Mode */
        #rage-overlay {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            box-shadow: inset 0 0 0px rgba(255, 0, 0, 0); pointer-events: none;
            transition: box-shadow 0.3s; z-index: 8;
        }
        #rage-overlay.active {
            box-shadow: inset 0 0 150px rgba(255, 0, 0, 0.4);
        }
        #rage-alert {
            position: absolute; top: 120px; left: 50%; transform: translateX(-50%);
            color: var(--red); font-family: var(--title-font); font-size: 24px;
            letter-spacing: 5px; opacity: 0; 
        }
        #rage-alert.active { animation: flicker 0.2s infinite; opacity: 1; }
        @keyframes flicker { 0% {opacity:1;} 50% {opacity:0.2;} 100% {opacity:0.9;} }
        
        .rage-dur { height: 4px; background: var(--red); width: 100%; margin-top: 5px; display: none;}

        /* Cinematic Effects */
        #cutscene-screen {
            justify-content: center; background: #000; transition: opacity 0.5s;
        }
        #cinematic-text {
            font-family: var(--title-font); font-size: 28px; letter-spacing: 8px;
            text-align: center; opacity: 1; color: #fff;
        }
        
        .glitch-flash {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background: #fff; opacity: 0; pointer-events: none; z-index: 100;
        }
        
        /* Run Zone UI */
        #run-ui {
            position: absolute; top: 20px; right: 20px; font-family: var(--mono-font); 
            display: none; text-align: right; pointer-events: none; z-index: 10;
        }
        
        /* Mobile Controls */
        .mobile-controls {
            display: none; position: absolute; bottom: 20px; left: 0; width: 100%;
            justify-content: space-between; padding: 0 20px; z-index: 50; pointer-events: none;
        }
        .dpad, .action-pad { display: flex; gap: 10px; pointer-events: all;}
        .mob-btn { width: 50px; height: 50px; border-radius: 50%; background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.3);}
        @media (max-width: 800px) {
            #game-wrapper { width: 100vw; height: 100vh; border: none;}
            .mobile-controls { display: flex; }
        }
    </style>
</head>
<body>
"""

html_body = """
    <div id="game-wrapper">
        <div id="parallax-bg"></div>
        <div id="rage-overlay"></div>
        <canvas id="gameCanvas" width="800" height="600"></canvas>
        <div id="glitch-flash" class="glitch-flash"></div>
        
        <!-- Run UI -->
        <div id="run-ui">
            <div id="run-dist">DISTANCE: 0M</div>
            <div id="run-orbs" style="color: #fff; margin-top:5px;">ORBS: 0</div>
        </div>

        <!-- Combat HUD -->
        <div id="hud">
            <div class="hud-top">
                <div class="hp-container">
                    <div class="fighter-name">YOU <span id="player-title" class="fighter-title"></span></div>
                    <div class="hp-bar"><div id="player-hp" class="hp-fill" style="width:100%"></div></div>
                    <div id="rage-timer" class="rage-dur"></div>
                </div>
                <div class="center-hud">
                    <div id="round-display" class="round-text">ZONE 1</div>
                </div>
                <div class="hp-container" style="align-items: flex-end;">
                    <div class="fighter-name">PHANTOM</div>
                    <div class="hp-bar"><div id="phantom-hp" class="hp-fill" style="width:100%"></div></div>
                </div>
            </div>
            <div id="rage-alert">RAGE MODE</div>
            <div class="corruption-container">
                <div class="corr-label">AI ASSIMILATION</div>
                <div class="corruption-bar"><div id="corruption-fill"></div></div>
            </div>
            
            <div class="mobile-controls">
                <div class="dpad">
                    <button class="mob-btn" id="btn-left">◀</button>
                    <button class="mob-btn" id="btn-right">▶</button>
                </div>
                <div class="action-pad">
                    <button class="mob-btn" id="btn-atk">ATK / JUMP</button>
                    <button class="mob-btn" id="btn-def">DEF / SLIDE</button>
                    <button class="mob-btn" id="btn-dash">DASH</button>
                </div>
            </div>
        </div>

        <div id="ui-layer">
            <!-- Main Menu -->
            <div id="main-menu" class="screen active">
                <h1 class="title-glitch">PHANTOM V</h1>
                <p class="subtitle">RUN. ADAPT. SURVIVE.</p>
                
                <div class="player-stats">
                    <div id="menu-name">FIGHTER</div>
                    <div id="menu-rank" class="rank-display">UNRANKED</div>
                    <div id="menu-sp" class="sp-display">0 SP</div>
                    <div style="font-size: 12px; margin-top: 10px; opacity: 0.5;">W: <span id="menu-w">0</span> | L: <span id="menu-l">0</span></div>
                </div>

                <button id="btn-enter-arena">COMMENCE RUN</button>
                <button id="btn-sanctum">THE SANCTUM</button>
            </div>

            <!-- Sanctum Menu -->
            <div id="sanctum-screen" class="screen">
                <div class="sanctum-header">
                    <h2>THE SANCTUM</h2>
                    <div id="sanctum-sp" class="sp-display" style="font-size: 20px;">0 SP</div>
                </div>
                
                <div class="tabs">
                    <button class="tab-btn active" data-target="tab-weapons">WEAPONS</button>
                    <button class="tab-btn" data-target="tab-lore">LORE</button>
                    <button class="tab-btn" data-target="tab-arenas">ARENAS</button>
                    <button class="tab-btn" data-target="tab-titles">TITLES</button>
                </div>

                <div id="tab-weapons" class="tab-content active"></div>
                <div id="tab-lore" class="tab-content"></div>
                <div id="tab-arenas" class="tab-content"></div>
                <div id="tab-titles" class="tab-content"></div>

                <button id="btn-back-main" style="margin-top: 20px;">RETURN</button>
            </div>

            <!-- Cutscene Screen -->
            <div id="cutscene-screen" class="screen">
                <div id="cinematic-text"></div>
            </div>
            
            <!-- Result Screen -->
            <div id="result-screen" class="screen">
                <h1 id="result-title">DEFEATED</h1>
                <p id="result-msg" style="margin-bottom: 20px; font-family: monospace;">YOU DIED IN THE WASTELAND</p>
                <div id="result-sp" class="sp-display" style="margin-bottom: 30px;">+0 SP</div>
                <button id="btn-return-menu">RETURN</button>
            </div>
        </div>
    </div>
"""

js_storage = """
    <script>
        /**
         * STORAGE & DATA ARCHITECTURE (Unchanged per request)
         */
        const DB_KEY = 'phantomV_save_data';
        
        const DEFAULT_STATE = {
            totalSP: 0,
            wins: 0,
            losses: 0,
            rankIndex: 0,
            unlockedWeapons: ['wpn_default'],
            unlockedLore: [],
            unlockedArenas: ['arena_default'],
            unlockedTitles: ['title_default'],
            equippedWeapon: 'wpn_default',
            equippedArena: 'arena_default',
            equippedTitle: 'title_default',
            phantomProfile: {
                dodgeLeft: 0, dodgeRight: 0,
                attackCounts: [],
                blockCount: 0,
                rageActivations: 0,
                openings: [],
                roundsObserved: 0
            }
        };

        const RANKS = [
            { name: 'UNRANKED', req: 0, color: '#aaaaaa' },
            { name: 'FRACTURED', req: 3, color: '#ffffff' },
            { name: 'HOLLOW', req: 8, color: '#ffffff' },
            { name: 'PHANTOM', req: 15, color: '#ffffff' },
            { name: 'VOID', req: 25, color: '#ffffff' }
        ];

        const ITEM_DATA = {
            weapons: [
                { id: 'wpn_default', name: 'Iron Blade', cost: 0, desc: 'Default, balanced' },
                { id: 'wpn_void', name: 'Void Cleaver', cost: 100, desc: '+15% damage, -10% speed' },
                { id: 'wpn_echo', name: 'Echo Gauntlet', cost: 200, desc: 'Copies PHANTOM last attack damage' },
                { id: 'wpn_edge', name: 'Phantom Edge', cost: 350, desc: '20% chance to phase through block' },
                { id: 'wpn_shatter', name: 'Shatter Staff', cost: 500, desc: 'Breaks guard on 3rd consecutive hit' }
            ],
            lore: [
                { id: 'lore_1', name: 'Entry 1', cost: 50, desc: '"PHANTOM was not built. It was left behind."' },
                { id: 'lore_2', name: 'Entry 2', cost: 100, desc: '"Every player who fought here fed it something."' },
                { id: 'lore_3', name: 'Entry 3', cost: 200, desc: '"It does not want to win. It wants to become."' },
                { id: 'lore_4', name: 'Entry 4', cost: 300, desc: '"You are not the first. The others never came back."' },
                { id: 'lore_5', name: 'Entry 5', cost: 500, desc: '"PHANTOM is what remains when a fighter stops growing."' }
            ],
            arenas: [
                { id: 'arena_default', name: 'Default', cost: 0, desc: 'Standard dark arena' },
                { id: 'arena_void', name: 'VOID', cost: 150, desc: 'Pure black, white energy floor' },
                { id: 'arena_crimson', name: 'CRIMSON', cost: 250, desc: 'Deep red arena, ember particles' },
                { id: 'arena_static', name: 'STATIC', cost: 400, desc: 'Glitchy TV static background' },
                { id: 'arena_abyss', name: 'ABYSS', cost: 600, desc: 'Infinite dark depth illusion' }
            ],
            titles: [
                { id: 'title_default', name: 'Unranked', cost: 0, desc: 'Default' },
                { id: 'title_hunter', name: 'Ghost Hunter', cost: 100, desc: 'Requires 3 wins', cond: s => s.wins >= 3 },
                { id: 'title_breaker', name: 'Mirror Breaker', cost: 250, desc: 'Requires 5 wins', cond: s => s.wins >= 5 },
                { id: 'title_slayer', name: 'Phantom Slayer', cost: 600, desc: 'Requires 10 wins', cond: s => s.wins >= 10 },
                { id: 'title_void', name: 'VOID', cost: 1000, desc: 'Requires 20 wins', cond: s => s.wins >= 20 }
            ]
        };

        class StorageManager {
            constructor() { this.load(); }
            load() {
                const data = localStorage.getItem(DB_KEY);
                this.state = data ? { ...DEFAULT_STATE, ...JSON.parse(data) } : { ...DEFAULT_STATE };
                this.checkRank();
            }
            save() { localStorage.setItem(DB_KEY, JSON.stringify(this.state)); }
            
            addSP(amount) { this.state.totalSP += amount; this.save(); }
            spendSP(amount) {
                if (this.state.totalSP >= amount) {
                    this.state.totalSP -= amount;
                    this.save(); return true;
                }
                return false;
            }
            
            checkRank() {
                let rIdx = 0;
                for(let i=RANKS.length-1; i>=0; i--) {
                    if (this.state.wins >= RANKS[i].req) { rIdx = i; break; }
                }
                this.state.rankIndex = rIdx;
            }

            unlockItem(category, id, cost) {
                const list = this.state['unlocked' + category.charAt(0).toUpperCase() + category.slice(1)];
                if (!list.includes(id) && this.spendSP(cost)) {
                    list.push(id);
                    this.save();
                    return true;
                }
                return false;
            }
            
            logMatch(won) {
                if (won) this.state.wins++; else this.state.losses++;
                this.checkRank();
                this.save();
            }
        }
        
        const storage = new StorageManager();
"""

js_ui = """
        /**
         * UI CONTROLLER
         */
        const Screens = {
            main: document.getElementById('main-menu'),
            sanctum: document.getElementById('sanctum-screen'),
            hud: document.getElementById('hud'),
            cutscene: document.getElementById('cutscene-screen'),
            result: document.getElementById('result-screen')
        };
        
        const equipMap = {
            weapons: 'equippedWeapon',
            arenas: 'equippedArena',
            titles: 'equippedTitle'
        };

        function showScreen(name) {
            Object.values(Screens).forEach(s => s.classList.remove('active'));
            if (name === 'hud') Screens.hud.style.display = 'block';
            else {
                Screens.hud.style.display = 'none';
                if(Screens[name]) Screens[name].classList.add('active');
            }
        }

        function updateMainMenu() {
            document.getElementById('menu-sp').textContent = storage.state.totalSP + ' SP';
            document.getElementById('menu-w').textContent = storage.state.wins;
            document.getElementById('menu-l').textContent = storage.state.losses;
            const rank = RANKS[storage.state.rankIndex];
            const rElem = document.getElementById('menu-rank');
            rElem.textContent = rank.name;
        }

        function renderSanctumTab(category) {
            const container = document.getElementById('tab-' + category);
            container.innerHTML = '';
            const items = ITEM_DATA[category];
            const unlockedList = storage.state['unlocked' + category.charAt(0).toUpperCase() + category.slice(1)];
            
            let equipped = category==="lore" ? null : storage.state[equipMap[category]];

            document.getElementById('sanctum-sp').textContent = storage.state.totalSP + ' SP';

            items.forEach(item => {
                const isUnlocked = unlockedList.includes(item.id);
                const isEquipped = equipped === item.id;
                const card = document.createElement('div');
                card.className = `item-card ${isEquipped ? 'equipped' : ''}`;
                
                let actionHTML = '';
                if (isUnlocked) {
                    if (category === 'lore') actionHTML = `<span>UNLOCKED</span>`;
                    else actionHTML = `<button class="equip-btn" data-id="${item.id}" ${isEquipped ? 'disabled' : ''}>${isEquipped ? 'EQUIPPED' : 'EQUIP'}</button>`;
                } else {
                    let canBuy = storage.state.totalSP >= item.cost;
                    if (item.cond && !item.cond(storage.state)) canBuy = false;
                    actionHTML = `<button class="buy-btn" data-id="${item.id}" data-cost="${item.cost}" ${canBuy ? '' : 'disabled'}>${item.cost} SP</button>`;
                }

                card.innerHTML = `
                    <div class="item-info">
                        <h3>${item.name}</h3>
                        <p>${category === 'lore' && !isUnlocked ? '???' : item.desc}</p>
                    </div>
                    <div class="item-action">${actionHTML}</div>
                `;
                container.appendChild(card);
            });

            container.querySelectorAll('.buy-btn').forEach(btn => {
                btn.onclick = (e) => {
                    if (storage.unlockItem(category, e.target.dataset.id, parseInt(e.target.dataset.cost))) {
                        renderSanctumTab(category);
                    }
                }
            });
            container.querySelectorAll('.equip-btn').forEach(btn => {
                btn.onclick = (e) => {
                    storage.state[equipMap[category]] = e.target.dataset.id;
                    storage.save(); renderSanctumTab(category);
                }
            });
        }

        document.getElementById('btn-sanctum').onclick = () => { showScreen('sanctum'); renderSanctumTab('weapons'); };
        document.getElementById('btn-back-main').onclick = () => { updateMainMenu(); showScreen('main'); };
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.onclick = (e) => {
                document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
                document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
                btn.classList.add('active');
                document.getElementById(btn.dataset.target).classList.add('active');
                renderSanctumTab(btn.dataset.target.split('-')[1]);
            };
        });
        document.getElementById('btn-return-menu').onclick = () => { updateMainMenu(); showScreen('main'); };
        
        updateMainMenu();
"""

js_input = """
        class InputHandler {
            constructor() {
                this.keys = {}; this.mouseClicked = false;
                window.addEventListener('keydown', e => this.keys[e.code] = true);
                window.addEventListener('keyup', e => this.keys[e.code] = false);
                
                // Fix Bug 4: mobile buttons
                const bindBtn = (id, key) => {
                    const btn = document.getElementById(id);
                    if(btn) {
                        btn.addEventListener('touchstart', e=>{e.preventDefault(); this.keys[key]=true;});
                        btn.addEventListener('touchend', e=>{e.preventDefault(); this.keys[key]=false;});
                        btn.addEventListener('mousedown', e=>{e.preventDefault(); this.keys[key]=true;});
                        btn.addEventListener('mouseup', e=>{e.preventDefault(); this.keys[key]=false;});
                    }
                };
                bindBtn('btn-left', 'ArrowLeft'); bindBtn('btn-right', 'ArrowRight');
                bindBtn('btn-atk', 'Space'); bindBtn('btn-def', 'ShiftLeft'); bindBtn('btn-dash', 'KeyQ');
            }
            isPressed(code) { return !!this.keys[code]; }
            getMovement() {
                let dx = 0, dy = 0;
                if (this.isPressed('ArrowLeft') || this.isPressed('KeyA')) dx -= 1;
                if (this.isPressed('ArrowRight') || this.isPressed('KeyD')) dx += 1;
                return { dx, dy };
            }
            isAttacking() { return this.isPressed('Space'); }
            isDefending() { return this.isPressed('ShiftLeft') || this.isPressed('ShiftRight'); }
            isDodging() { return this.isPressed('KeyQ'); }
        }
"""

js_engine = """
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        const CONFIG = { WIDTH: 800, HEIGHT: 600, FLOOR_Y: 500, ACTIONS: { IDLE: 'idle', ATTACK: 'attack', DODGE: 'dodge', DEFEND: 'defend' } };

        class ParticleSystem {
            constructor() { this.particles = []; this.shakeTime = 0; this.shakeMag = 0; }
            shake(mag, time) { this.shakeMag = mag; this.shakeTime = time; }
            burst(x, y, colorStr, count) {
                for(let i=0; i<count; i++) {
                    const ang = Math.random() * Math.PI * 2;
                    const speed = 2 + Math.random() * 5;
                    this.particles.push({
                        x, y, vx: Math.cos(ang)*speed, vy: Math.sin(ang)*speed,
                        life: 1.0, color: colorStr, size: 2 + Math.random()*4
                    });
                }
            }
            update(dt) {
                if(this.shakeTime > 0) this.shakeTime -= dt;
                for(let i=this.particles.length-1; i>=0; i--) {
                    let p = this.particles[i];
                    p.x += p.vx; p.y += p.vy;
                    p.life -= dt * 1.5;
                    if(p.life <= 0) this.particles.splice(i, 1);
                }
            }
            applyShake(ctx) {
                if (this.shakeTime > 0) {
                    const dx = (Math.random()-0.5)*this.shakeMag;
                    const dy = (Math.random()-0.5)*this.shakeMag;
                    ctx.translate(dx, dy);
                }
            }
            draw(ctx) {
                this.particles.forEach(p => {
                    ctx.globalAlpha = p.life; ctx.fillStyle = p.color;
                    ctx.beginPath(); ctx.arc(p.x, p.y, p.size, 0, Math.PI*2); ctx.fill();
                });
                ctx.globalAlpha = 1.0;
            }
        }

        class Entity {
            constructor(x, color) {
                this.x = x; this.y = CONFIG.FLOOR_Y;
                this.w = 40; this.h = 70;
                this.color = color;
                this.health = 100;
                this.action = CONFIG.ACTIONS.IDLE;
                this.vx = 0; this.vy = 0;
                
                // Run Zone specifically
                this.isJumping = false;
                this.canDoubleJump = false;
                this.isSliding = false;
                
                // Arena specifically
                this.baseSpeed = 200;
                this.baseDmg = 10;
                this.speedMult = 1.0;
                this.dmgMult = 1.0;
                
                this.attackCooldown = 0;
                this.dodgeCooldown = 0;
                this.isDefending = false;
                this.flashTime = 0;
            }
            
            get totalSpeed() { return this.baseSpeed * this.speedMult; }
            get totalDmg() { return this.baseDmg * this.dmgMult; }
            
            takeDamage(amt) {
                if(this.isDefending) amt *= 0.4;
                this.health = Math.max(0, this.health - amt);
                this.flashTime = 0.1;
                return amt;
            }
            
            updateArena(dt) {
                if(this.attackCooldown > 0) this.attackCooldown -= dt;
                if(this.dodgeCooldown > 0) this.dodgeCooldown -= dt;
                if(this.flashTime > 0) this.flashTime -= dt;
                this.x = Math.max(50, Math.min(750, this.x + this.vx * dt * this.totalSpeed));
            }
            
            updateRunner(dt) {
                // Gravity
                this.vy += 1200 * dt;
                this.y += this.vy * dt;
                if (this.y >= CONFIG.FLOOR_Y) {
                    this.y = CONFIG.FLOOR_Y; this.vy = 0;
                    this.isJumping = false; this.canDoubleJump = true;
                }
                
                // Slide Hitbox adjusting
                if (this.isSliding) this.h = 35;
                else this.h = 70;
            }

            drawFigure(ctx, colorOverride, isFlipped = false) {
                const color = colorOverride || this.color;
                const baseOpacity = ctx.globalAlpha;
                ctx.save(); ctx.fillStyle = color; ctx.strokeStyle = color;
                ctx.lineCap = 'round'; ctx.lineJoin = 'round';

                let headRadius = 12;
                let headY = this.y - this.h + headRadius;
                let neckY = headY + headRadius;
                let neckX = this.x; const baseWidth = 35; 

                let leanAngle = 0; let armAngle = 0.5; let weaponAngle = 0;
                let attackTrail = 0;

                if (this.isSliding) {
                    leanAngle = Math.PI/2 - 0.2; neckY += 20; headY += 20; // Flatten down
                } else if (this.isJumping) {
                    leanAngle = -0.2; armAngle = -1.0;
                }
                
                if (this.action === CONFIG.ACTIONS.ATTACK) {
                    const t = 1 - Math.max(0, this.attackCooldown / 0.4);
                    let easedT = 0;
                    if (t < 0.2) easedT = -0.3 * (t/0.2); 
                    else if (t < 0.4) { const snap = (t-0.2)/0.2; easedT = snap; attackTrail = 1-snap; }
                    else easedT = 1;
                    
                    leanAngle = 0.3 * easedT;
                    const startAngle = -Math.PI * 0.75; const endAngle = Math.PI * 0.25;
                    armAngle = startAngle + (endAngle - startAngle) * easedT;
                    weaponAngle = armAngle;
                } else if (this.isDefending) {
                    leanAngle = -0.1; armAngle = -0.3; weaponAngle = -Math.PI * 0.4;
                } else if (this.action === CONFIG.ACTIONS.DODGE) {
                    leanAngle = 0.4; armAngle = 0.8;
                }
                
                if (isFlipped) leanAngle *= -1;
                ctx.translate(neckX, this.y); ctx.rotate(leanAngle); ctx.translate(-neckX, -this.y);

                const frontDir = isFlipped ? -1 : 1; const backDir = isFlipped ? 1 : -1;
                
                // Minimal Body
                ctx.beginPath(); ctx.moveTo(neckX, neckY);
                ctx.quadraticCurveTo(neckX + (backDir*10), neckY+15, neckX + (backDir*baseWidth/2), this.y);
                ctx.lineTo(neckX + (frontDir*baseWidth/2), this.y);
                ctx.quadraticCurveTo(neckX + (frontDir*2), neckY+20, neckX, neckY);
                ctx.fill();
                
                // Head
                ctx.beginPath(); ctx.arc(neckX + (frontDir*2), headY, headRadius, 0, Math.PI*2); ctx.fill();
                
                // Arm
                const armY = neckY + 4; const armLen = 22;
                const finalArmAngle = isFlipped ? Math.PI - armAngle : armAngle;
                const handX = neckX + Math.cos(finalArmAngle) * armLen;
                const handY = armY + Math.sin(finalArmAngle) * armLen;
                ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(neckX, armY); ctx.lineTo(handX, handY); ctx.stroke();

                if(!this.isSliding && !this.isJumping) {
                    this.drawWeapon(ctx, handX, handY, weaponAngle, color, isFlipped);
                }

                // Shield
                if (this.isDefending) {
                    ctx.globalAlpha = baseOpacity * 0.6; ctx.lineWidth = 2; ctx.beginPath();
                    const sX = neckX + (frontDir*20); const sY = this.y - this.h/1.8;
                    ctx.arc(sX, sY, this.h/1.4, isFlipped ? Math.PI*0.7 : -Math.PI*0.3, isFlipped ? Math.PI*1.3 : Math.PI*0.3); 
                    ctx.stroke();
                }
                ctx.restore();
            }

            drawWeapon(ctx, x, y, angle, color, isFlipped) {
                ctx.save(); ctx.translate(x, y); ctx.rotate(isFlipped ? -angle+Math.PI : angle);
                ctx.strokeStyle = color; ctx.lineWidth = 2; 
                ctx.beginPath(); ctx.moveTo(0,0); ctx.lineTo(35,0); ctx.stroke();
                ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(3,-6); ctx.lineTo(3,6); ctx.stroke();
                ctx.restore();
            }

            draw(ctx, isFlipped) {
                ctx.save();
                if(this.flashTime > 0) ctx.globalAlpha = 0.5;
                this.drawFigure(ctx, this.color, isFlipped);
                ctx.restore();
            }
        }
"""

js_ai = """
        class PhantomAI {
            constructor(enemyRef, playerRef) {
                this.phantom = enemyRef;
                this.player = playerRef;
                this.prof = storage.state.phantomProfile;
                this.timer = 0;
                this.arenaLevel = 1; // 1 to 5
            }
            
            update(dt) {
                this.timer -= dt;
                // Update Corruption Bar for visuals
                let corr = Math.min(100, this.prof.roundsObserved * 15 + this.prof.dodgeLeft*2 + this.prof.blockCount*2);
                document.getElementById('corruption-fill').style.width = corr + '%';

                if(this.timer > 0) return;
                this.phantom.vx = 0;
                this.phantom.isDefending = false;
                this.phantom.action = CONFIG.ACTIONS.IDLE;
                
                const dist = this.player.x - this.phantom.x;
                const absDist = Math.abs(dist);
                
                // Behavior based on Arena Level
                if (this.arenaLevel === 1) {
                    // Level 0: Dumb
                    if (absDist > 70) {
                        this.phantom.vx = Math.sign(dist) * this.phantom.speed * 0.5; // Slow
                        this.timer = 0.5;
                    } else {
                        if (Math.random() < 0.3 && this.phantom.attackCooldown <= 0) {
                            this.phantom.action = CONFIG.ACTIONS.ATTACK;
                            this.phantom.attackCooldown = 0.8;
                            this.timer = 0.8;
                        }
                    }
                } 
                else if (this.arenaLevel === 2) {
                    // Level 1: Learning
                    if (absDist > 70) {
                        this.phantom.vx = Math.sign(dist) * this.phantom.speed * 0.8;
                        this.timer = 0.3;
                    } else {
                        if (this.player.action === CONFIG.ACTIONS.ATTACK && Math.random() < 0.3) {
                            this.phantom.isDefending = true; this.timer = 0.4;
                        } else if (Math.random() < 0.5 && this.phantom.attackCooldown <= 0) {
                            this.phantom.action = CONFIG.ACTIONS.ATTACK; this.phantom.attackCooldown = 0.6; this.timer = 0.6;
                        }
                    }
                }
                else {
                    // Level 2, 3, MAX: Adapting/Dangerous
                    const aggro = (this.arenaLevel * 0.25);
                    if (absDist > 70) {
                        if (Math.random() < aggro) {
                            this.phantom.vx = Math.sign(dist) * this.phantom.speed; this.timer = 0.2;
                        } else {
                            this.phantom.isDefending = Math.random() > 0.5; this.timer = 0.4;
                        }
                    } else {
                        if (this.player.action === CONFIG.ACTIONS.ATTACK && this.player.attackCooldown > 0) {
                            if (Math.random() < aggro) { this.phantom.isDefending = true; this.timer = 0.3; }
                            else { this.phantom.x -= Math.sign(dist)*60; this.timer = 0.4; this.phantom.action = CONFIG.ACTIONS.DODGE; }
                        } else {
                            if (Math.random() < aggro && this.phantom.attackCooldown <= 0) {
                                // Specific Counters
                                if (this.arenaLevel >= 4 && this.prof.rageActivations >= 2 && this.player.health > 25 && this.player.health < 40) {
                                    this.phantom.isDefending = true; this.timer = 0.5; return; // Bleed bait
                                }
                                if (this.arenaLevel >= 4 && this.player.isDefending && this.prof.blockCount > 10) {
                                    this.phantom.dmgMult = 2.0; // Guard Break
                                } else { this.phantom.dmgMult = 1.0; }

                                this.phantom.action = CONFIG.ACTIONS.ATTACK; this.phantom.attackCooldown = 0.4; this.timer = 0.4;
                            } else {
                                this.phantom.isDefending = true; this.timer = 0.3;
                            }
                        }
                    }
                }
            }
        }
"""

js_game = """
        class GameMaster {
            constructor() {
                this.input = new InputHandler();
                this.vfx = new ParticleSystem();
                this.lastTime = performance.now();
                this.state = 'menu'; // menu, cin_to_run, run, cin_to_arena, arena, gameover
                this.zone = 1;
                this.reqFrame = null;
                
                this.player = new Entity(150, '#ffffff');
                this.phantom = new Entity(650, '#ff0000');
                this.ai = new PhantomAI(this.phantom, this.player);
                
                this.obstacles = [];
                this.orbs = [];
                this.runDistance = 0;
                this.orbCount = 0;
                
                this.gameOver = false;
                this.rageActive = false;
                this.rageTimer = 0;
                this.bgOffset = 0;
                
                document.getElementById('btn-enter-arena').onclick = () => this.startGame();
            }

            startGame() {
                this.zone = 1;
                this.startRunZone();
                if(!this.reqFrame) this.loop(performance.now());
            }
            
            showCinematic(text, nextStateCallback) {
                this.state = 'cutscene';
                showScreen('cutscene');
                const tEl = document.getElementById('cinematic-text');
                tEl.textContent = text;
                setTimeout(() => { showScreen('hud'); nextStateCallback(); }, 3000);
            }

            // ======== RUN ZONE ========
            startRunZone() {
                this.showCinematic(`ZONE ${this.zone}`, () => {
                    this.state = 'run';
                    this.runDistance = 0;
                    this.orbCount = 0;
                    this.obstacles = [];
                    this.orbs = [];
                    this.player.x = 200;
                    this.player.y = CONFIG.FLOOR_Y;
                    this.player.health = 100;
                    this.gameOver = false;
                    document.getElementById('run-ui').style.display = 'block';
                    document.querySelector('.hp-container').style.display = 'none';
                    document.querySelectorAll('.hp-container')[1].style.display = 'none';
                    document.querySelector('.corruption-container').style.display = 'none';
                    document.getElementById('round-display').textContent = `ZONE ${this.zone}`;
                });
            }
            
            generateObstacle() {
                const type = Math.random();
                let obsX = 850;
                if (type < 0.4) {
                    // Gap
                    this.obstacles.push({ x: obsX, w: 100, type: 'gap' });
                } else if (type < 0.7) {
                    // High barrier (must slide)
                    this.obstacles.push({ x: obsX, w: 20, y: CONFIG.FLOOR_Y - 90, h: 90, type: 'high' });
                } else {
                    // Low barrier (must jump)
                    this.obstacles.push({ x: obsX, w: 30, h: 40, type: 'low' });
                }
                
                if (Math.random() < 0.5) {
                    this.orbs.push({ x: obsX + 50, y: CONFIG.FLOOR_Y - 100, active: true });
                }
            }

            updateRun(dt) {
                if(this.gameOver) return;
                
                // Auto run right
                const runSpeed = 300 + (this.zone * 20); // gets faster
                this.bgOffset += runSpeed * dt;
                this.runDistance += (runSpeed * dt) / 100;
                
                document.getElementById('run-dist').textContent = `DISTANCE: ${Math.floor(this.runDistance)}M / ${50 + this.zone*20}M`;
                document.getElementById('run-orbs').textContent = `ORBS: ${this.orbCount}`;

                // Win Zone Condition
                const targetDist = 50 + this.zone * 20;
                if (this.runDistance >= targetDist) {
                    storage.addSP(20);
                    this.startArena();
                    return;
                }

                // Input
                if (this.input.isAttacking() && !this.player.isJumping) {
                    this.player.vy = -600; this.player.isJumping = true; this.player.isSliding = false;
                } else if (this.input.isAttacking() && this.player.isJumping && this.player.canDoubleJump && this.player.vy > -200) {
                    this.player.vy = -500; this.player.canDoubleJump = false;
                }
                
                if (this.input.isDefending() && !this.player.isJumping) {
                    this.player.isSliding = true;
                } else { this.player.isSliding = false; }
                
                this.player.updateRunner(dt);

                // Obstacles & Collision
                if (Math.random() < 0.02 * this.zone) this.generateObstacle();

                for(let i=this.obstacles.length-1; i>=0; i--) {
                    let o = this.obstacles[i];
                    o.x -= runSpeed * dt;
                    if(o.x < -100) { this.obstacles.splice(i, 1); continue; }
                    
                    // Collision check
                    let pRight = this.player.x + this.player.w/2;
                    let pLeft = this.player.x - this.player.w/2;
                    let pBottom = this.player.y;
                    let pTop = this.player.y - this.player.h;

                    if (o.type === 'gap') {
                        if (pRight > o.x && pLeft < o.x + o.w && pBottom >= CONFIG.FLOOR_Y) {
                            this.triggerRunDeath(); return;
                        }
                    } else if (o.type === 'low') {
                        let oTop = CONFIG.FLOOR_Y - o.h;
                        if (pRight > o.x && pLeft < o.x + o.w && pBottom > oTop) {
                            this.triggerRunDeath(); return;
                        }
                    } else if (o.type === 'high') {
                        // Sliding required. High barrier starts Y down to floor-90. Meaning it occupies top space.
                        // Actually let's make high barrier occupy Top to Floor-35
                        let gapY = CONFIG.FLOOR_Y - 40; // Slide height is 35
                        if (pRight > o.x && pLeft < o.x + o.w && pTop < gapY) {
                            this.triggerRunDeath(); return;
                        }
                    }
                }
                
                // Orbs
                for(let i=this.orbs.length-1; i>=0; i--) {
                    let orb = this.orbs[i];
                    orb.x -= runSpeed * dt;
                    if(orb.active && Math.abs(this.player.x - orb.x) < 30 && Math.abs((this.player.y - this.player.h/2) - orb.y) < 30) {
                        orb.active = false; this.orbCount++; storage.addSP(5);
                    }
                    if(orb.x < -50) this.orbs.splice(i, 1);
                }
            }

            triggerRunDeath() {
                this.gameOver = true; this.state = 'gameover';
                document.getElementById('run-ui').style.display = 'none';
                setTimeout(() => {
                    Screens.hud.style.display = 'none';
                    Screens.result.classList.add('active');
                    document.getElementById('result-title').textContent = 'KILLED';
                    document.getElementById('result-msg').textContent = 'YOU FAILED THE OBSTACLES';
                    document.getElementById('result-sp').textContent = '+0 SP';
                }, 1000);
            }

            // ======== ARENA ZONE ========
            startArena() {
                const enterText = ["IT IS WATCHING YOU", "IT REMEMBERS YOUR FACE", "IT LEARNED FROM YOU", "IT HAS STUDIED YOU", "NOW FINISH IT"][this.zone-1] || "PREPARE";
                this.showCinematic(enterText, () => {
                    this.state = 'arena';
                    this.gameOver = false;
                    this.player.x = 150; this.player.y = CONFIG.FLOOR_Y; this.player.action = CONFIG.ACTIONS.IDLE;
                    this.phantom.x = 650; this.phantom.y = CONFIG.FLOOR_Y; this.phantom.health = 100;
                    this.ai.arenaLevel = this.zone;

                    document.getElementById('run-ui').style.display = 'none';
                    document.querySelector('.hp-container').style.display = 'flex';
                    document.querySelectorAll('.hp-container')[1].style.display = 'flex';
                    document.querySelector('.corruption-container').style.display = 'block';
                    document.getElementById('round-display').textContent = this.zone === 5 ? 'FINAL ARENA' : `ARENA ${this.zone}`;
                });
            }

            updateArena(dt) {
                if(this.gameOver) return;

                const move = this.input.getMovement();
                this.player.vx = move.dx;
                this.player.isDefending = this.input.isDefending();
                
                if(!this.player.isDefending && this.input.isAttacking() && this.player.attackCooldown <= 0) {
                    this.player.action = CONFIG.ACTIONS.ATTACK; this.player.attackCooldown = 0.4;
                    storage.state.phantomProfile.attackCounts.push(this.timeElapsed);
                } else if(!this.player.isDefending && this.input.isDodging() && this.player.dodgeCooldown <= 0) {
                    this.player.action = CONFIG.ACTIONS.DODGE;
                    const dDist = move.dx !== 0 ? Math.sign(move.dx)*100 : (this.player.x<400?100:-100);
                    this.player.x += dDist; this.player.dodgeCooldown = 0.8;
                    if(dDist<0) storage.state.phantomProfile.dodgeLeft++; else storage.state.phantomProfile.dodgeRight++;
                } else { this.player.action = CONFIG.ACTIONS.IDLE; }

                if (this.player.isDefending) storage.state.phantomProfile.blockCount += dt*10;

                // Fix 3: Rage Multipliers
                if (!this.rageActive && this.player.health <= 25 && this.rageTimer <= -3) {
                    this.rageActive = true; this.rageTimer = 10;
                    storage.state.phantomProfile.rageActivations++;
                    this.player.speedMult = 1.4; this.player.dmgMult = 1.5;
                    document.getElementById('rage-overlay').classList.add('active');
                }
                
                if (this.rageActive) {
                    this.rageTimer -= dt;
                    if (this.rageTimer <= 0) {
                        this.rageActive = false; this.rageTimer = -3;
                        this.player.speedMult = 0.8; this.player.dmgMult = 1.0;
                        document.getElementById('rage-overlay').classList.remove('active');
                    }
                } else if (this.rageTimer < 0 && this.rageTimer > -3 && !this.rageActive) {
                    this.rageTimer += dt;
                    if(this.rageTimer >= 0) { this.player.speedMult = 1.0; this.rageTimer = 0; }
                }

                this.player.updateArena(dt);
                this.ai.update(dt);
                this.phantom.updateArena(dt);
                
                this.checkCombat();
            }
            
            checkCombat() {
                // Fix 1: check gameOver instantly
                if(this.gameOver) return;
                
                if (Math.abs(this.player.x - this.phantom.x) < 70) {
                    if (this.player.action === CONFIG.ACTIONS.ATTACK && this.player.attackCooldown > 0.3) {
                        this.phantom.takeDamage(this.player.totalDmg);
                        this.vfx.shake(5, 0.2); this.player.action = CONFIG.ACTIONS.IDLE; 
                    }
                    if (this.phantom.action === CONFIG.ACTIONS.ATTACK && this.phantom.attackCooldown > 0.3) {
                        this.player.takeDamage(this.phantom.totalDmg);
                        this.vfx.shake(5, 0.2); this.phantom.action = CONFIG.ACTIONS.IDLE;
                    }
                }

                document.getElementById('player-hp').style.width = `${this.player.health}%`;
                document.getElementById('phantom-hp').style.width = `${this.phantom.health}%`;

                if (this.phantom.health <= 0) {
                    this.gameOver = true; this.player.action = CONFIG.ACTIONS.IDLE; this.player.attackCooldown = 0;
                    storage.state.phantomProfile.roundsObserved++;
                    storage.addSP(30);
                    if (this.zone >= 5) this.triggerArenaOver(true);
                    else {
                        this.zone++;
                        const winText = ["IT SAW EVERYTHING", "IT FELT THAT", "IT SAW WHAT YOU DID", "YOU ALWAYS DO THAT"][this.zone-2] || "CLEAR";
                        this.showCinematic(winText, () => this.startRunZone());
                    }
                } else if (this.player.health <= 0) {
                    this.gameOver = true; this.player.action = CONFIG.ACTIONS.IDLE; this.player.attackCooldown = 0;
                    this.triggerArenaOver(false);
                }
            }
            
            triggerArenaOver(won) {
                this.state = 'gameover';
                document.getElementById('rage-overlay').classList.remove('active');
                setTimeout(() => {
                    Screens.hud.style.display = 'none';
                    Screens.result.classList.add('active');
                    document.getElementById('result-title').textContent = won ? 'YOU DEFEATED YOURSELF' : 'DEFEATED';
                    document.getElementById('result-msg').textContent = won ? 'THE MIRROR SHATTERS' : 'YOU TAUGHT ME EVERYTHING';
                    storage.logMatch(won);
                }, 2000);
            }

            update(time) {
                const dt = Math.min((time - this.lastTime) / 1000, 0.1);
                this.lastTime = time;
                this.vfx.update(dt);
                
                if (this.state === 'run') this.updateRun(dt);
                else if (this.state === 'arena') this.updateArena(dt);
            }

            render() {
                ctx.clearRect(0, 0, CONFIG.WIDTH, CONFIG.HEIGHT);
                ctx.save();
                this.vfx.applyShake(ctx);

                // Floor
                ctx.strokeStyle = '#fff'; ctx.lineWidth = 1; ctx.beginPath();
                ctx.moveTo(0, CONFIG.FLOOR_Y); ctx.lineTo(CONFIG.WIDTH, CONFIG.FLOOR_Y); ctx.stroke();

                if (this.state === 'run') {
                    // Draw lines indicating run speed
                    ctx.strokeStyle = 'rgba(255,255,255,0.2)';
                    for(let i=0; i<10; i++) {
                        let lineX = (i*100 - (this.bgOffset % 100));
                        ctx.beginPath(); ctx.moveTo(lineX, CONFIG.FLOOR_Y); ctx.lineTo(lineX - 50, CONFIG.FLOOR_Y + 50); ctx.stroke();
                    }
                    
                    if(!this.gameOver) this.player.draw(ctx, false);
                    
                    // Obstacles
                    this.obstacles.forEach(o => {
                        ctx.fillStyle = '#fff';
                        if(o.type === 'gap') { ctx.fillStyle = '#000'; ctx.fillRect(o.x, CONFIG.FLOOR_Y-2, o.w, 5); }
                        else if(o.type === 'low') { ctx.fillRect(o.x, CONFIG.FLOOR_Y - o.h, o.w, o.h); }
                        else if(o.type === 'high') { ctx.fillRect(o.x, o.y, o.w, o.h); }
                    });
                    
                    // Orbs
                    this.orbs.forEach(orb => {
                        if(orb.active) {
                            ctx.fillStyle = '#00d4ff'; ctx.beginPath(); ctx.arc(orb.x, orb.y, 8, 0, Math.PI*2); ctx.fill();
                        }
                    });

                } else if (this.state === 'arena') {
                    if(this.player.health > 0) this.player.draw(ctx, false);
                    if(this.phantom.health > 0) this.phantom.draw(ctx, true);
                }
                
                this.vfx.draw(ctx);
                ctx.restore();
            }

            loop(time) {
                this.update(time);
                this.render();
                this.reqFrame = requestAnimationFrame(t => this.loop(t));
            }
        }

        const engine = new GameMaster();
    </script>
</body>
</html>
"""

full_content = html_head + css_content + html_body + js_storage + js_ui + js_input + js_engine + js_ai + js_game

with open("index.html", "w", encoding="utf-8") as f:
    f.write(full_content)
