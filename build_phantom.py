import os

html_head = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PHANTOM - Psychological Combat</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;700&family=Share+Tech+Mono&display=swap" rel="stylesheet">
"""

css_content = """
    <style>
        :root {
            --bg-color: #050505;
            --player-color: #ffffff;
            --cyan: #00d4ff;
            --blue: #0099ff;
            --amber: #ffaa00;
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
            box-shadow: 0 0 50px rgba(0, 212, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.05);
            background: var(--arena-bg);
            overflow: hidden;
        }
        
        #arena-background {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            pointer-events: none;
            z-index: 1;
            transition: all 1s;
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
            background: rgba(5, 5, 5, 0.95);
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
            background: rgba(255,255,255,0.1);
            border-color: var(--cyan);
            box-shadow: 0 0 15px rgba(0, 212, 255, 0.3);
        }
        button:disabled {
            opacity: 0.3;
            cursor: not-allowed;
            border-color: #333;
            box-shadow: none;
        }

        /* Main Menu */
        .title-glitch {
            font-size: 64px;
            letter-spacing: 15px;
            margin-bottom: 5px;
            text-shadow: 0 0 20px var(--cyan);
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
        .rank-display { color: var(--cyan); font-weight: bold; font-size: 18px; margin-top: 5px;}
        .sp-display { color: var(--purple); margin-top: 5px;}

        /* Sanctum Menu */
        #sanctum-screen { justify-content: flex-start; padding: 30px; }
        .sanctum-header {
            width: 100%; display: flex; justify-content: space-between; align-items: center;
            margin-bottom: 20px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 15px;
        }
        .tabs { display: flex; gap: 10px; margin-bottom: 20px; }
        .tab-btn { border: none; border-bottom: 2px solid transparent; padding: 10px 20px; }
        .tab-btn.active { border-bottom-color: var(--cyan); background: rgba(0,212,255,0.1); }
        .tab-content { width: 100%; height: 400px; display: none; overflow-y: auto; }
        .tab-content.active { display: flex; flex-direction: column; gap: 10px; }
        
        .item-card {
            display: flex; justify-content: space-between; align-items: center;
            padding: 15px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1);
        }
        .item-card.equipped { border-color: var(--cyan); background: rgba(0,212,255,0.05); }
        .item-info h3 { margin-bottom: 5px; }
        .item-info p { font-family: var(--mono-font); font-size: 12px; opacity: 0.7; }
        .lock-status { font-family: var(--mono-font); color: var(--amber); }

        /* HUD */
        #hud {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            pointer-events: none; padding: 20px; display: none; z-index: 10;
        }
        .hud-top { display: flex; justify-content: space-between; align-items: flex-start; }
        .hp-container { display: flex; flex-direction: column; width: 200px; }
        .fighter-name { font-family: var(--title-font); font-size: 16px; margin-bottom: 5px; text-shadow: 0 0 5px rgba(255,255,255,0.5);}
        .hp-bar { width: 100%; height: 12px; background: rgba(255,255,255,0.1); position: relative; border: 1px solid rgba(255,255,255,0.2); }
        .hp-fill { height: 100%; transition: width 0.1s; }
        #player-hp { background: var(--cyan); box-shadow: 0 0 10px var(--cyan); }
        #phantom-hp { background: var(--red); box-shadow: 0 0 10px var(--red); }
        .fighter-title { font-size: 10px; opacity: 0.6; margin-top: 2px; }

        .center-hud { text-align: center; }
        .round-text { font-family: var(--title-font); font-size: 20px; letter-spacing: 2px;}
        
        .corruption-container { position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%); text-align: center; width: 300px;}
        .corruption-bar { height: 4px; background: rgba(255,0,0,0.2); margin-top: 5px; position:relative; overflow: hidden;}
        #corruption-fill { height: 100%; background: var(--red); width: 0%; box-shadow: 0 0 10px var(--red); transition: width 0.5s;}
        .corr-label { font-size: 12px; letter-spacing: 2px; color: var(--red); opacity: 0.8;}

        /* Rage Mode */
        #rage-overlay {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            box-shadow: inset 0 0 100px rgba(255, 0, 0, 0); pointer-events: none;
            transition: box-shadow 0.3s; z-index: 8;
        }
        #rage-overlay.active {
            box-shadow: inset 0 0 150px rgba(255, 0, 0, 0.4);
            animation: pulse-rage 1s infinite alternate;
        }
        @keyframes pulse-rage {
            from { box-shadow: inset 0 0 100px rgba(255, 0, 0, 0.2); }
            to { box-shadow: inset 0 0 180px rgba(255, 0, 0, 0.6); }
        }
        #rage-alert {
            position: absolute; top: 120px; left: 50%; transform: translateX(-50%);
            color: var(--red); font-family: var(--title-font); font-size: 24px;
            letter-spacing: 5px; opacity: 0; text-shadow: 0 0 10px var(--red);
        }
        #rage-alert.active { animation: flicker 0.2s infinite; opacity: 1; }
        @keyframes flicker { 0% {opacity:1;} 50% {opacity:0.2;} 100% {opacity:0.9;} }
        
        .rage-dur { height: 4px; background: var(--red); width: 100%; margin-top: 5px; display: none;}

        /* Cinematic Effects */
        #cinematic-text {
            position: absolute; top: 40%; left: 50%; transform: translate(-50%, -50%);
            font-family: var(--title-font); font-size: 32px; letter-spacing: 10px;
            text-align: center; opacity: 0; transition: opacity 0.5s; z-index: 20; text-shadow: 0 0 20px #fff;
        }
        
        .glitch-flash {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background: #fff; opacity: 0; pointer-events: none; z-index: 100;
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
        <div id="arena-background"></div>
        <div id="rage-overlay"></div>
        <canvas id="gameCanvas" width="800" height="600"></canvas>
        <div id="glitch-flash" class="glitch-flash"></div>
        <div id="cinematic-text"></div>
        
        <!-- HUD -->
        <div id="hud">
            <div class="hud-top">
                <div class="hp-container">
                    <div class="fighter-name">YOU <span id="player-title" class="fighter-title"></span></div>
                    <div class="hp-bar"><div id="player-hp" class="hp-fill" style="width:100%"></div></div>
                    <div id="rage-timer" class="rage-dur"></div>
                </div>
                <div class="center-hud">
                    <div id="round-display" class="round-text">ROUND 1</div>
                </div>
                <div class="hp-container" style="align-items: flex-end;">
                    <div class="fighter-name">PHANTOM</div>
                    <div class="hp-bar"><div id="phantom-hp" class="hp-fill" style="width:100%"></div></div>
                </div>
            </div>
            <div id="rage-alert">RAGE MODE</div>
            <div class="corruption-container">
                <div class="corr-label">CORRUPTION</div>
                <div class="corruption-bar"><div id="corruption-fill"></div></div>
            </div>
            
            <div class="mobile-controls">
                <div class="dpad">
                    <button class="mob-btn" id="btn-left">◀</button>
                    <button class="mob-btn" id="btn-right">▶</button>
                </div>
                <div class="action-pad">
                    <button class="mob-btn" id="btn-atk" style="background:rgba(0,212,255,0.2)">ATK</button>
                    <button class="mob-btn" id="btn-def" style="background:rgba(255,255,255,0.2)">DEF</button>
                    <button class="mob-btn" id="btn-dash">DASH</button>
                </div>
            </div>
        </div>

        <div id="ui-layer">
            <!-- Main Menu -->
            <div id="main-menu" class="screen active">
                <h1 class="title-glitch">PHANTOM</h1>
                <p class="subtitle">IT DOES NOT GET STRONGER. IT GETS SMARTER.</p>
                
                <div class="player-stats">
                    <div id="menu-name">FIGHTER</div>
                    <div id="menu-rank" class="rank-display">UNRANKED</div>
                    <div id="menu-sp" class="sp-display">0 SP</div>
                    <div style="font-size: 12px; margin-top: 10px; opacity: 0.5;">W: <span id="menu-w">0</span> | L: <span id="menu-l">0</span></div>
                </div>

                <button id="btn-enter-arena">ENTER ARENA</button>
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

            <!-- Pre-fight screen -->
            <div id="pre-fight" class="screen">
                <h1 id="fight-round-text">ROUND 1</h1>
                <h3 id="fight-phase-text" style="color:var(--cyan); margin-top:10px;">PHASE 1: OBSERVE</h3>
            </div>
            
            <!-- Result Screen -->
            <div id="result-screen" class="screen">
                <h1 id="result-title">DEFEATED</h1>
                <p id="result-msg" style="margin-bottom: 20px; font-family: monospace;">YOU TAUGHT ME EVERYTHING</p>
                <div id="result-sp" class="sp-display" style="margin-bottom: 30px;">+10 SP</div>
                <button id="btn-return-menu">RETURN</button>
            </div>
        </div>
    </div>
"""

js_storage = """
    <script>
        /**
         * STORAGE & DATA ARCHITECTURE
         */
        const DB_KEY = 'phantom_save_data';
        
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
            { name: 'HOLLOW', req: 8, color: '#0099ff' },
            { name: 'PHANTOM', req: 15, color: '#aa00ff' },
            { name: 'VOID', req: 25, color: '#ff0000' }
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
            prefight: document.getElementById('pre-fight'),
            result: document.getElementById('result-screen')
        };

        function showScreen(name) {
            Object.values(Screens).forEach(s => s.classList.remove('active'));
            if (name === 'hud') Screens.hud.style.display = 'flex';
            else {
                Screens.hud.style.display = 'none';
                if(Screens[name]) Screens[name].classList.add('active');
            }
        }

        // Update Main Menu
        function updateMainMenu() {
            document.getElementById('menu-sp').textContent = storage.state.totalSP + ' SP';
            document.getElementById('menu-w').textContent = storage.state.wins;
            document.getElementById('menu-l').textContent = storage.state.losses;
            
            const rank = RANKS[storage.state.rankIndex];
            const rElem = document.getElementById('menu-rank');
            rElem.textContent = rank.name;
            rElem.style.color = rank.color;
        }

        // Render Sanctum Tab
        function renderSanctumTab(category) {
            const container = document.getElementById('tab-' + category);
            container.innerHTML = '';
            const items = ITEM_DATA[category];
            const unlockedList = storage.state['unlocked' + category.charAt(0).toUpperCase() + category.slice(1)];
            const equippedProp = 'equipped' + category.charAt(0).toUpperCase() + category.slice(1,-1); // naive
            let equipped = category==="lore" ? null : (category==="weapons" ? storage.state.equippedWeapon : (category==="arenas" ? storage.state.equippedArena : storage.state.equippedTitle));

            document.getElementById('sanctum-sp').textContent = storage.state.totalSP + ' SP';

            items.forEach(item => {
                const isUnlocked = unlockedList.includes(item.id);
                const isEquipped = equipped === item.id;
                
                const card = document.createElement('div');
                card.className = `item-card ${isEquipped ? 'equipped' : ''}`;
                
                let actionHTML = '';
                if (isUnlocked) {
                    if (category === 'lore') {
                        actionHTML = `<span style="color:var(--cyan)">UNLOCKED</span>`;
                    } else {
                        actionHTML = `<button class="equip-btn" data-id="${item.id}" ${isEquipped ? 'disabled' : ''}>${isEquipped ? 'EQUIPPED' : 'EQUIP'}</button>`;
                    }
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

            // Bind buttons
            container.querySelectorAll('.buy-btn').forEach(btn => {
                btn.onclick = (e) => {
                    const id = e.target.dataset.id;
                    const cost = parseInt(e.target.dataset.cost);
                    if (storage.unlockItem(category, id, cost)) {
                        renderSanctumTab(category);
                    }
                }
            });
            container.querySelectorAll('.equip-btn').forEach(btn => {
                btn.onclick = (e) => {
                    const id = e.target.dataset.id;
                    if (category === 'weapons') storage.state.equippedWeapon = id;
                    if (category === 'arenas') storage.state.equippedArena = id;
                    if (category === 'titles') storage.state.equippedTitle = id;
                    storage.save();
                    renderSanctumTab(category);
                }
            });
        }

        // Init UI listeners
        document.getElementById('btn-sanctum').onclick = () => {
            showScreen('sanctum');
            renderSanctumTab('weapons');
        };
        document.getElementById('btn-back-main').onclick = () => {
            updateMainMenu();
            showScreen('main');
        };
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.onclick = (e) => {
                document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
                document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
                btn.classList.add('active');
                const target = btn.dataset.target;
                document.getElementById(target).classList.add('active');
                renderSanctumTab(target.split('-')[1]);
            };
        });
        
        document.getElementById('btn-enter-arena').onclick = () => {
            startGame();
        };
        document.getElementById('btn-return-menu').onclick = () => {
            updateMainMenu();
            showScreen('main');
        };
        
        updateMainMenu();
"""

js_engine = """
        /**
         * GAME ENGINE & COMBAT
         */
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        const CONFIG = {
            WIDTH: 800, HEIGHT: 600, FLOOR_Y: 500,
            ACTIONS: { IDLE: 'idle', ATTACK: 'attack', DODGE: 'dodge', DEFEND: 'defend' }
        };

        class InputHandler {
            constructor() {
                this.keys = {};
                this.mouseClicked = false;
                window.addEventListener('keydown', e => this.keys[e.code] = true);
                window.addEventListener('keyup', e => this.keys[e.code] = false);
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
                    ctx.globalAlpha = p.life;
                    ctx.fillStyle = p.color;
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
                this.maxHealth = 100;
                this.action = CONFIG.ACTIONS.IDLE;
                this.vx = 0; this.speed = 200; // px/s
                this.attackCooldown = 0;
                this.dodgeCooldown = 0;
                this.isDefending = false;
                this.flashTime = 0;
                
                // Modifiers
                this.baseDmg = 10;
                this.dmgMult = 1.0;
                this.speedMult = 1.0;
            }
            
            takeDamage(amt) {
                if(this.isDefending) amt *= 0.4;
                this.health = Math.max(0, this.health - amt);
                this.flashTime = 0.1;
                return amt;
            }
            
            update(dt) {
                if(this.attackCooldown > 0) this.attackCooldown -= dt;
                if(this.dodgeCooldown > 0) this.dodgeCooldown -= dt;
                if(this.flashTime > 0) this.flashTime -= dt;
                
                this.x = Math.max(50, Math.min(750, this.x + this.vx * dt * this.speedMult));
            }

            drawFigure(ctx, colorOverride, isFlipped = false) {
                const color = colorOverride || this.color;
                const baseOpacity = ctx.globalAlpha;
                ctx.save(); ctx.fillStyle = color; ctx.strokeStyle = color;
                ctx.lineCap = 'round'; ctx.lineJoin = 'round';

                const headRadius = 12;
                const headY = this.y - this.h + headRadius;
                const neckY = headY + headRadius;
                const neckX = this.x; const baseWidth = 35; 

                let leanAngle = 0; let armAngle = 0.5; let weaponAngle = 0;
                let attackTrail = 0;

                if (this.action === CONFIG.ACTIONS.ATTACK) {
                    const t = 1 - Math.max(0, this.attackCooldown / 0.4);
                    let easedT = 0;
                    if (t < 0.2) easedT = -0.3 * (t/0.2); 
                    else if (t < 0.4) { const snap = (t-0.2)/0.2; easedT = snap; attackTrail = 1-snap; }
                    else easedT = 1 + 0.1 * Math.sin(((t - 0.4) / 0.6) * Math.PI); 
                    
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
                // Cloak
                ctx.beginPath(); ctx.moveTo(neckX, neckY);
                ctx.quadraticCurveTo(neckX + (backDir*20), neckY+15, neckX + (backDir*baseWidth/2), this.y);
                ctx.lineTo(neckX + (frontDir*baseWidth/2), this.y);
                ctx.quadraticCurveTo(neckX + (frontDir*5), neckY+20, neckX, neckY);
                ctx.fill();
                // Head
                ctx.beginPath(); ctx.arc(neckX + (frontDir*5), headY, headRadius, 0, Math.PI*2); ctx.fill();
                
                // Arm
                const armY = neckY + 4; const armLen = 22;
                const finalArmAngle = isFlipped ? Math.PI - armAngle : armAngle;
                const handX = neckX + Math.cos(finalArmAngle) * armLen;
                const handY = armY + Math.sin(finalArmAngle) * armLen;
                ctx.lineWidth = 6; ctx.beginPath(); ctx.moveTo(neckX, armY); ctx.lineTo(handX, handY); ctx.stroke();

                // Weapon
                this.drawWeapon(ctx, handX, handY, weaponAngle, color, isFlipped);
                
                // Action Trail / Motion Blur for the overhead slash
                if (attackTrail > 0) {
                    ctx.save();
                    ctx.globalAlpha = baseOpacity * attackTrail * 0.6;
                    ctx.strokeStyle = color === '#ffffff' ? '#00d4ff' : color;
                    ctx.lineWidth = 12;
                    ctx.lineCap = 'round';
                    ctx.beginPath();
                    
                    const trailRadius = armLen + 45; 
                    const traceCenterY = armY;
                    const endArc = isFlipped ? Math.PI - weaponAngle : weaponAngle;
                    const startArc = isFlipped ? Math.PI - (-Math.PI * 0.75) : -Math.PI * 0.75; 
                    
                    const antiClockwise = isFlipped ? true : false; 
                    
                    ctx.arc(neckX, traceCenterY, trailRadius * 0.8, startArc, endArc, antiClockwise);
                    ctx.stroke();
                    ctx.restore();
                }

                // Shield
                if (this.isDefending) {
                    ctx.globalAlpha = baseOpacity * 0.6;
                    ctx.strokesStyle = color === '#ffffff' ? '#00d4ff' : color;
                    ctx.lineWidth = 4; ctx.beginPath();
                    const sX = neckX + (frontDir*20); const sY = this.y - this.h/1.8;
                    const r = this.h/1.4;
                    const st = isFlipped ? Math.PI*0.7 : -Math.PI*0.3;
                    const en = isFlipped ? Math.PI*1.3 : Math.PI*0.3;
                    ctx.arc(sX, sY, r, st, en); ctx.stroke();
                    
                    ctx.globalAlpha = baseOpacity * 0.2;
                    ctx.lineWidth = 12;
                    ctx.beginPath();
                    ctx.arc(sX, sY, r - 2, st, en);
                    ctx.stroke();
                }
                ctx.restore();
            }

            drawWeapon(ctx, x, y, angle, color, isFlipped) {
                ctx.save(); ctx.translate(x, y); ctx.rotate(isFlipped ? -angle+Math.PI : angle);
                ctx.shadowBlur = 10; ctx.shadowColor = color; ctx.strokeStyle = color;
                ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(0,0); ctx.lineTo(45,0); ctx.stroke();
                ctx.lineWidth = 5; ctx.beginPath(); ctx.moveTo(5,-8); ctx.lineTo(5,8); ctx.stroke();
                ctx.restore();
            }

            draw(ctx, isFlipped) {
                ctx.save();
                if(this.flashTime > 0) ctx.globalAlpha = 0.5;
                // Glow
                ctx.shadowBlur = 15; ctx.shadowColor = this.color;
                this.drawFigure(ctx, this.color, isFlipped);
                ctx.shadowBlur = 0;
                this.drawFigure(ctx, '#ffffff', isFlipped);
                ctx.restore();
            }
        }
"""

js_ai_system = """
        class PhantomAI {
            constructor(enemyRef, playerRef) {
                this.phantom = enemyRef;
                this.player = playerRef;
                this.prof = storage.state.phantomProfile;
                this.state = 'idle';
                this.timer = 0;
                this.corruption = 0; // 0 to 100
                this.roundPhase = 1; // 1=Observe, 2=Adapt, 3=Hunt
                this.knowledge = []; // Active learned counters
                
                this.colorBase = '#ffffff';
                this.updateColor();
            }
            
            updateColor() {
                const pct = this.corruption;
                // Transition White -> Grey -> Dark Red -> Black
                const red = pct < 50 ? (255 - pct*2) : (155 + (pct-50)*2);
                const gb  = pct < 50 ? (255 - pct*5) : (5 + (50-pct)*0.1); 
                this.phantom.color = `rgb(${red},${gb},${gb})`;
            }
            
            evaluatePlayer() {
                // Determine counters based on profile
                this.knowledge = [];
                if (this.prof.dodgeLeft > this.prof.dodgeRight * 1.5) this.knowledge.push('bait_left');
                if (this.prof.dodgeRight > this.prof.dodgeLeft * 1.5) this.knowledge.push('bait_right');
                if (this.prof.blockCount > 10) this.knowledge.push('guard_break');
                if (this.prof.rageActivations >= 2) this.knowledge.push('bleed_bait');
                
                this.corruption = Math.min(100, this.prof.roundsObserved * 33 + this.knowledge.length * 10);
                this.updateColor();
            }

            update(dt) {
                this.timer -= dt;
                
                const dist = this.player.x - this.phantom.x;
                const absDist = Math.abs(dist);
                
                // Corruption logic (learning)
                if (this.roundPhase === 1) {
                    this.corruption = Math.min(100, this.corruption + dt * 0.5);
                    this.updateColor();
                    document.getElementById('corruption-fill').style.width = this.corruption + '%';
                }
                
                if(this.timer > 0) return; // Busy
                
                // Simple AI state machine
                this.phantom.vx = 0;
                this.phantom.isDefending = false;
                this.phantom.action = CONFIG.ACTIONS.IDLE;
                
                // Aggression scales with Round Phase (1 to 3)
                const aggro = (this.roundPhase * 0.3); 

                if (absDist > 70) {
                    // Close distance
                    if (Math.random() < aggro) {
                        this.phantom.vx = Math.sign(dist) * this.phantom.speed;
                        this.timer = 0.2;
                    } else {
                        // Observe
                        this.phantom.isDefending = Math.random() > 0.5;
                        this.timer = 0.5;
                    }
                } else {
                    // In combat range
                    if (this.player.action === CONFIG.ACTIONS.ATTACK && this.player.attackCooldown > 0) {
                        // Player is attacking, decide to block or dodge
                        if (Math.random() < (0.3 * this.roundPhase)) {
                            this.phantom.isDefending = true;
                            this.timer = 0.3;
                        } else {
                            // Dodge
                            this.phantom.x -= Math.sign(dist) * 60;
                            this.timer = 0.4;
                            this.phantom.action = CONFIG.ACTIONS.DODGE;
                        }
                    } else {
                        // Attack
                        if (Math.random() < aggro && this.phantom.attackCooldown <= 0) {
                            
                            // Check Knowledge
                            if (this.knowledge.includes('bleed_bait') && this.player.health > 25 && this.player.health < 40) {
                                // Wait for rage
                                this.phantom.isDefending = true;
                                this.timer = 0.5;
                                return;
                            }
                            
                            if (this.knowledge.includes('guard_break') && this.player.isDefending) {
                                // Simulate heavy hit
                                this.phantom.dmgMult = 2.0;
                            } else {
                                this.phantom.dmgMult = 1.0;
                            }

                            this.phantom.action = CONFIG.ACTIONS.ATTACK;
                            this.phantom.attackCooldown = 0.4;
                            this.timer = 0.4;
                        } else {
                            // Wait
                            this.phantom.isDefending = true;
                            this.timer = 0.3;
                        }
                    }
                }
            }
        }
"""

js_game = """
        class GameEngine {
            constructor() {
                this.input = new InputHandler();
                this.vfx = new ParticleSystem();
                this.lastTime = performance.now();
                this.state = 'menu';
                this.reqFrame = null;
                
                // Combat state
                this.round = 1;
                this.timeElapsed = 0;
                this.gameOver = false;
                this.rageActive = false;
                this.rageTimer = 0;
                this.discipline = true; // Win without rage bonus
            }

            start() {
                this.player = new Entity(150, '#00d4ff');
                this.phantom = new Entity(650, '#ffaa00');
                
                // Apply player weapon
                const wpn = storage.state.equippedWeapon;
                if(wpn === 'wpn_void') { this.player.dmgMult = 1.15; this.player.speedMult = 0.9; }

                // Apply Title
                const titleObj = ITEM_DATA.titles.find(t => t.id === storage.state.equippedTitle);
                document.getElementById('player-title').textContent = `[${titleObj ? titleObj.name : 'Unranked'}]`;

                this.ai = new PhantomAI(this.phantom, this.player);
                this.ai.evaluatePlayer();
                this.ai.roundPhase = 1;
                
                this.round = 1;
                this.timeElapsed = 0;
                this.gameOver = false;
                this.discipline = true;
                
                showScreen('hud');
                this.state = 'playing';
                this.showPreFight();
                
                this.lastTime = performance.now();
                if(!this.reqFrame) this.loop(performance.now());
            }

            showPreFight() {
                this.state = 'prefight';
                Screens.prefight.classList.add('active');
                document.getElementById('fight-phase-text').textContent = 
                    this.round === 1 ? 'PHASE 1: OBSERVE' : (this.round === 2 ? 'PHASE 2: ADAPT' : 'PHASE 3: HUNT');
                document.getElementById('fight-round-text').textContent = `ROUND ${this.round}`;
                
                setTimeout(() => {
                    Screens.prefight.classList.remove('active');
                    this.state = 'playing';
                }, 2000);
            }

            update(time) {
                const dt = Math.min((time - this.lastTime) / 1000, 0.1);
                this.lastTime = time;
                this.vfx.update(dt);
                
                if (this.state !== 'playing' || this.gameOver) return;

                this.timeElapsed += dt;

                // Player Input
                const move = this.input.getMovement();
                this.player.vx = move.dx * this.player.speed;
                this.player.isDefending = this.input.isDefending();
                
                if(!this.player.isDefending && this.input.isAttacking() && this.player.attackCooldown <= 0) {
                    this.player.action = CONFIG.ACTIONS.ATTACK;
                    this.player.attackCooldown = 0.4;
                    storage.state.phantomProfile.attackCounts.push(this.timeElapsed);
                } else if(!this.player.isDefending && this.input.isDodging() && this.player.dodgeCooldown <= 0) {
                    this.player.action = CONFIG.ACTIONS.DODGE;
                    const dashDist = move.dx !== 0 ? Math.sign(move.dx)*100 : (this.player.x < 400 ? 100 : -100);
                    this.player.x += dashDist;
                    this.player.dodgeCooldown = 0.8;
                    if(dashDist < 0) storage.state.phantomProfile.dodgeLeft++;
                    else storage.state.phantomProfile.dodgeRight++;
                } else {
                    this.player.action = CONFIG.ACTIONS.IDLE;
                }

                if (this.player.isDefending) storage.state.phantomProfile.blockCount += dt*10;

                // Rage Logic
                if (!this.rageActive && this.player.health > 0 && this.player.health <= 25 && this.rageTimer <= -3) {
                    this.rageActive = true;
                    this.discipline = false; // Used rage
                    this.rageTimer = 10;
                    storage.state.phantomProfile.rageActivations++;
                    this.player.speedMult += 0.4;
                    this.player.dmgMult += 0.5;
                    document.getElementById('rage-overlay').classList.add('active');
                    document.getElementById('rage-alert').classList.add('active');
                    document.querySelector('.rage-dur').style.display = 'block';
                }
                
                if (this.rageActive) {
                    this.rageTimer -= dt;
                    document.getElementById('rage-timer').style.width = `${(this.rageTimer/10)*100}%`;
                    if (this.rageTimer <= 0) {
                        this.rageActive = false;
                        this.rageTimer = -3; // Exhaustion
                        this.player.speedMult -= 0.6; // Net -0.2
                        this.player.dmgMult -= 0.5;
                        document.getElementById('rage-overlay').classList.remove('active');
                        document.getElementById('rage-alert').classList.remove('active');
                        document.querySelector('.rage-dur').style.display = 'none';
                    }
                } else if (this.rageTimer < 0 && this.rageTimer > -3 && !this.rageActive) {
                    this.rageTimer += dt;
                    if(this.rageTimer >= 0) { this.player.speedMult += 0.6; this.rageTimer = 0; } // Restore normal
                }

                this.player.update(dt);
                
                // AI Update
                this.ai.update(dt);
                this.phantom.update(dt);

                // Check Combat
                this.checkCombat();
            }

            checkCombat() {
                if(this.gameOver) return;
                
                const dist = Math.abs(this.player.x - this.phantom.x);
                if (dist < 70) {
                    // Quick hit registration (active frames 0-0.1s of attack)
                    // We only register attack in first few frames
                    const isPlAtk = this.player.action === CONFIG.ACTIONS.ATTACK && this.player.attackCooldown > 0.3;
                    const isPhAtk = this.phantom.action === CONFIG.ACTIONS.ATTACK && this.phantom.attackCooldown > 0.3;
                    
                    if (isPlAtk) {
                        this.phantom.takeDamage(this.player.baseDmg * this.player.dmgMult);
                        this.vfx.shake(8, 0.2);
                        this.player.action = CONFIG.ACTIONS.IDLE; // Prevent multi-hit
                    }
                    if (isPhAtk) {
                        this.player.takeDamage(this.phantom.baseDmg * this.phantom.dmgMult);
                        this.vfx.shake(8, 0.2);
                        this.phantom.action = CONFIG.ACTIONS.IDLE;
                    }
                }

                // HUD Update
                document.getElementById('player-hp').style.width = `${this.player.health}%`;
                document.getElementById('phantom-hp').style.width = `${this.phantom.health}%`;

                if (this.phantom.health <= 0) {
                    if (this.round >= 3) {
                        this.triggerGameOver(true);
                    }
                    else {
                        this.round++;
                        storage.state.phantomProfile.roundsObserved++;
                        this.ai.roundPhase = this.round;
                        this.phantom.health = 100;
                        this.ai.evaluatePlayer();
                        this.showPreFight();
                    }
                } else if (this.player.health <= 0) {
                    this.triggerGameOver(false);
                }
            }

            triggerGameOver(playerWon) {
                this.gameOver = true;
                this.state = 'gameover';
                
                // VFX
                this.vfx.shake(20, 0.5);
                const deadEnt = playerWon ? this.phantom : this.player;
                this.vfx.burst(deadEnt.x, deadEnt.y - 35, playerWon ? '#ff0000' : '#00d4ff', 40);
                
                document.getElementById('glitch-flash').style.opacity = 1;
                setTimeout(() => document.getElementById('glitch-flash').style.opacity = 0, 100);

                // Rewards
                let spEarned = playerWon ? 150 : 10;
                if(playerWon && this.discipline) spEarned += 60; // Discipline bonus

                storage.logMatch(playerWon);
                storage.addSP(spEarned);

                setTimeout(() => {
                    Screens.hud.style.display = 'none';
                    document.getElementById('rage-overlay').classList.remove('active');
                    Screens.result.classList.add('active');
                    document.getElementById('result-title').textContent = playerWon ? 'YOU SURVIVED' : 'DEFEATED';
                    document.getElementById('result-title').style.color = playerWon ? 'var(--cyan)' : 'var(--red)';
                    document.getElementById('result-msg').textContent = playerWon ? "THIS ISN'T OVER. I REMEMBER." : "YOU TAUGHT ME EVERYTHING.";
                    document.getElementById('result-sp').textContent = `+${spEarned} SP`;
                }, 2000);
            }

            render() {
                ctx.clearRect(0, 0, CONFIG.WIDTH, CONFIG.HEIGHT);
                ctx.save();
                this.vfx.applyShake(ctx);
                
                // Floor
                ctx.strokeStyle = 'rgba(255, 255, 255, 0.2)';
                ctx.lineWidth = 2; ctx.beginPath();
                ctx.moveTo(0, CONFIG.FLOOR_Y); ctx.lineTo(CONFIG.WIDTH, CONFIG.FLOOR_Y); ctx.stroke();

                if (this.state === 'playing' || this.state === 'gameover' || this.state === 'prefight') {
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

        const engine = new GameEngine();
        function startGame() { engine.start(); }
    </script>
</body>
</html>
"""

full_content = html_head + css_content + html_body + js_storage + js_ui + js_engine + js_ai_system + js_game

with open("index.html", "w", encoding="utf-8") as f:
    f.write(full_content)
