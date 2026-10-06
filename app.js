const pages = {
  home: { section: 'Start here', title: 'Orthographic Projection', deck: 'A visual introduction to the drawing language used to describe real objects with clarity and precision.', render: homePage },
  'what-is': { section: 'Introduction', title: 'What is orthographic projection?', deck: 'A way to describe a three-dimensional object with accurate, flat views that can be measured and made.', render: whatIsPage },
  'how-works': { section: 'Introduction', title: 'How does it work?', deck: 'Parallel sight lines meet a picture plane at right angles, recording the true shape of each face.', render: howWorksPage },
  'how-many': { section: 'Introduction', title: 'How many views do we need?', deck: 'Choose enough views to describe every important part of the object, and no more than the drawing needs.', render: howManyPage },
  'first-angle': { section: 'Projection methods', title: 'First-angle projection', deck: 'In first-angle projection, the object sits between the observer and each projection plane.', render: () => anglePage('first') },
  'third-angle': { section: 'Projection methods', title: 'Third-angle projection', deck: 'In third-angle projection, each projection plane sits between the observer and the object.', render: () => anglePage('third') },
  'projection-symbols': { section: 'Projection methods', title: 'Reading the projection symbol', deck: 'The truncated cone symbol tells you how the views on a drawing have been arranged.', render: symbolsPage },
  'hidden-lines': { section: 'Drawing practice', title: 'Visible and hidden edges', deck: 'Line weight and line style show which edges you can see and which ones sit behind a surface.', render: hiddenLinesPage },
  sections: { section: 'Drawing practice', title: 'When a section helps', deck: 'A section view reveals interior detail when too many hidden lines make a drawing difficult to read.', render: sectionsPage },
  quiz: { section: 'Drawing practice', title: 'Test yourself', deck: 'Check the ideas from this module, then review the explanations for any answers you missed.', render: quizPage }
};

const navigation = [
  { type: 'link', id: 'home', label: 'Module home', icon: '⌂' },
  { type: 'group', id: 'intro-group', label: 'Introduction', icon: '01', children: [
    { id: 'what-is', label: 'What is orthographic projection?' },
    { id: 'how-works', label: 'How does it work?' },
    { id: 'how-many', label: 'How many views?' }
  ]},
  { type: 'group', id: 'projection-group', label: 'Projection methods', icon: '02', children: [
    { id: 'first-angle', label: 'First-angle projection' },
    { id: 'third-angle', label: 'Third-angle projection' },
    { id: 'projection-symbols', label: 'Projection symbols' }
  ]},
  { type: 'group', id: 'practice-group', label: 'Drawing practice', icon: '03', children: [
    { id: 'hidden-lines', label: 'Visible and hidden edges' },
    { id: 'sections', label: 'Section views' },
    { id: 'quiz', label: 'Test yourself' }
  ]}
];
const lessonOrder = ['what-is', 'how-works', 'how-many', 'first-angle', 'third-angle', 'projection-symbols', 'hidden-lines', 'sections', 'quiz'];
const progressKey = 'ortho-module-completed-v1';
let currentPage = 'home';

function pageLink(id, label, className = '') {
  return `<a class="${className}" href="?page=${id}" data-page="${id}">${label}</a>`;
}

function renderNavigation() {
  const nav = document.getElementById('lesson-nav');
  nav.innerHTML = navigation.map(item => {
    if (item.type === 'link') return `<a class="nav-home" href="?page=${item.id}" data-page="${item.id}"><span class="nav-icon">${item.icon}</span>${item.label}</a>`;
    return `<div class="nav-group" data-group="${item.id}"><button class="nav-group-button" type="button" aria-expanded="false"><span class="nav-icon">${item.icon}</span>${item.label}<span class="chevron" aria-hidden="true">›</span></button><div class="nav-children">${item.children.map(child => pageLink(child.id, child.label, 'nav-child')).join('')}</div></div>`;
  }).join('');
}

function shell(heading, content, aside = '') {
  return `<div class="page-heading"><p class="eyebrow">${heading.section} <span aria-hidden="true">/</span> FIELD GUIDE</p><h1>${heading.title}</h1><p class="deck">${heading.deck}</p></div><div class="page-layout"><article class="article-column">${content}</article><aside class="lesson-aside" aria-label="Lesson notes">${aside || standardAside(heading)}</aside></div>`;
}

function standardAside(heading) {
  return `<div class="aside-card"><p class="aside-label">Key idea</p><p><strong>${heading.section === 'Introduction' ? 'Describe form with views.' : heading.section === 'Projection methods' ? 'Arrangement matters.' : 'Make the drawing easy to read.'}</strong> Each view should add information the others do not already provide.</p><p class="aside-accent">Use the module menu to move between lessons. Your visited lessons are saved here.</p></div><div class="aside-card"><p class="aside-label">At the drawing board</p><p>Read a drawing from the visible edges first. Use the projection symbol to understand where the other views belong.</p></div>`;
}

function homePage() {
  return `<section class="home-hero"><div class="home-hero-copy"><p class="eyebrow">A VISUAL FIELD GUIDE · ENGINEERING GRAPHICS</p><h1>Make the shape clear.<br />Make every line count.</h1><p>Learn how engineers turn three-dimensional objects into accurate, readable drawings using orthographic views.</p>${pageLink('what-is', 'Begin the module <span class="arrow">↗</span>', 'primary-button')}</div><div class="home-hero-art" aria-hidden="true"><svg viewBox="0 0 360 190"><path class="plane" d="M202 21 333 91 202 163 72 91Z"/><path class="fine" d="M72 91v54l130 72 131-72V91M202 163v54M72 145l130-72 131 72" transform="translate(0 -42)"/><path class="object-face object-top" d="m138 70 48-27 48 27-48 27Z"/><path class="object-face" d="M138 70v58l48 27V97Z"/><path class="object-face object-face" d="M186 97v58l48-27V70Z"/><path class="axis" d="M186 97v-48m0 48 70 39M186 97l-70 39"/><path class="fine" d="m256 49 11 6m-81-19v-8m-81 63-13 7m201-7 12 7M186 155v22"/></svg></div></section>
  <div class="home-stats"><div class="home-stat"><strong>03</strong><span>Core views to start</span></div><div class="home-stat"><strong>02</strong><span>Projection systems</span></div><div class="home-stat"><strong>01</strong><span>Clear drawing standard</span></div></div>
  ${shell({section:'Module overview',title:'A drawing that travels well',deck:'A shared set of views lets a designer, engineer and maker understand the same object, even when they are far apart.'}, `<p class="lead-copy">Orthographic projection is the common language behind engineering drawings. It lets us describe an object with flat views that preserve its proportions and show its important details.</p><div class="topic-grid"><a class="topic-card" href="?page=what-is" data-page="what-is"><span class="topic-index">01 / FOUNDATION</span><h3>Build a picture from views</h3><p>Meet the method and see why a single view rarely tells the whole story.</p><span class="card-arrow">↗</span></a><a class="topic-card" href="?page=third-angle" data-page="third-angle"><span class="topic-index">02 / ARRANGEMENT</span><h3>Read the view layout</h3><p>Compare first-angle and third-angle projection by moving the views.</p><span class="card-arrow">↗</span></a><a class="topic-card" href="?page=hidden-lines" data-page="hidden-lines"><span class="topic-index">03 / LINEWORK</span><h3>Show what is out of sight</h3><p>Use line types to separate visible outlines from hidden edges.</p><span class="card-arrow">↗</span></a><a class="topic-card" href="?page=quiz" data-page="quiz"><span class="topic-index">04 / REVIEW</span><h3>Check your understanding</h3><p>Finish with a short quiz and see feedback for each answer.</p><span class="card-arrow">↗</span></a></div><div class="callout"><strong>How to use this module</strong>Move through the lessons in order, or open any topic from the menu. Try the controls beside each drawing: they reveal the ideas that a still image cannot show.</div>`, `<div class="aside-card"><p class="aside-label">Module route</p><p><strong>Foundation → Views → Methods → Linework</strong></p><p class="aside-accent">About 10 minutes · 9 short lessons</p></div><div class="aside-card"><p class="aside-label">Your progress</p><p>Visited topics are marked in the left menu. The module remembers progress in this browser.</p></div>`)}${endLinks('home')}`;
}

function projectionSvg(angle = 'third', options = {}) {
  const showHidden = options.showHidden !== false;
  const topY = angle === 'third' ? 27 : 208;
  const sideX = angle === 'third' ? 371 : 146;
  const frontShift = angle === 'third' ? 0 : 34;
  const sideLabel = 'RIGHT';
  return `<svg class="projection-svg" data-angle="${angle}" viewBox="0 0 560 300" role="img" aria-label="An isometric block beside its ${angle}-angle plan, front and side views"><defs><marker id="arrow-small" markerWidth="6" markerHeight="6" refX="3" refY="3" orient="auto"><path d="M0 0 6 3 0 6Z" fill="#a6b6ae"/></marker></defs>
    <g transform="translate(${angle === 'third' ? 14 : -1} 23)"><text x="4" y="12">OBJECT</text><path class="projection-line" d="M120 47 197 91M120 137 197 146M120 91 197 119"/><path class="model-face face-top" d="m30 81 55-31 58 32-56 33Z"/><path class="model-face face-front" d="M30 81v75l57 32v-73Z"/><path class="model-face face-side" d="M87 115v73l56-32V82Z"/><path class="detail" d="M57 66v40m28-56v42m-28 34 30-17m-30 35 30-17m28-42v73"/><path class="projection-line" d="M152 82v110"/><text x="41" y="213">3D FORM</text></g>
    <g class="view-layout ${options.unfolded ? 'unfolded' : ''}"><text x="241" y="17">ORTHOGRAPHIC VIEWS</text>
      <path class="projection-line" d="M334 110h27m-226 45h57m105-76v14m-91 76v15"/>
      <g data-view-name="plan" transform="translate(${frontShift} 0)"><path class="view" d="M226 ${topY}h104v66H226Z"/><path class="detail" d="M226 ${topY+22}h104m-70-22v66m36-66v66"/><text x="258" y="${topY+40}">PLAN</text></g>
      <g data-view-name="front" transform="translate(${frontShift} 0)"><path class="view" d="M226 111h104v74H226Z"/><path class="detail" d="M226 150h65v35m-65-35h24v-39m41 39v35"/><path class="hidden-edge" style="opacity:${showHidden ? '1':'0'}" d="M291 111v39m23-39v39"/><text x="259" y="152">FRONT</text></g>
      <g data-view-name="side"><path class="view" d="M${sideX} 111h89v74h-89Z"/><path class="detail" d="M${sideX} 150h89m-55-39v74"/><path class="hidden-edge" style="opacity:${showHidden ? '1':'0'}" d="M${sideX+63} 111v74"/><text x="${sideX+24}" y="152">${sideLabel}</text></g>
      <path class="projection-line accent-line" d="M${angle === 'third' ? 332 : 260} 148h${angle === 'third' ? 30 : -23}" marker-end="url(#arrow-small)"/>
    </g><text x="228" y="${angle === 'third' ? 280 : 288}" class="accent-label">${angle === 'third' ? 'TOP VIEW ABOVE · RIGHT VIEW TO THE RIGHT' : 'TOP VIEW BELOW · RIGHT VIEW TO THE LEFT'}</text>
  </svg>`;
}

function diagramCard(title, svg, caption, controls = '') {
  return `<figure class="lesson-figure"><div class="figure-head"><strong>${title}</strong><span>Interactive drawing</span></div>${svg}${controls ? `<div class="diagram-controls">${controls}</div>` : ''}<figcaption class="figure-caption">${caption}</figcaption></figure>`;
}

function whatIsPage() {
  const body = `<p class="lead-copy">Orthographic projection is a method of representing a three-dimensional object using two-dimensional views. Each view is made by looking squarely at one face of the object and projecting its visible edges onto a flat plane.</p>${diagramCard('One object, several true-shape views', projectionSvg('third'), 'The plan, front and side views each show a different face. Their outlines stay true to size and shape.', '')}<h2>Why use it?</h2><p>A perspective picture is useful for seeing an object as a whole, but its edges appear to converge and its measurements are harder to read. Orthographic views remove that perspective. They give the people designing, making and inspecting a part a consistent set of information.</p><div class="callout"><strong>A universal drawing language</strong>When a projection method is marked clearly, a drawing can be read across teams and countries. The lines and view positions carry the same meaning for everyone.</div><h2>What you will learn</h2><ul><li>How perpendicular projectors create each view.</li><li>How first-angle and third-angle layouts differ.</li><li>How to show hidden edges and internal detail.</li></ul>`;
  return shell(pages['what-is'], body) + endLinks('what-is');
}

function howWorksPage() {
  const body = `<p class="lead-copy">Imagine a flat sheet of glass placed in front of an object. Look straight at the object and trace the edges that are visible. The lines of sight are parallel to one another and meet the sheet at right angles.</p>${diagramCard('Projecting the front face onto a plane', `<svg class="projection-svg" viewBox="0 0 560 260" role="img" aria-label="Parallel sight lines project a block onto a vertical plane"><path class="plane" d="M355 29v183"/><path class="detail" d="M355 29v183m6-183v183"/><text x="372" y="45">PICTURE PLANE</text><path class="model-face face-top" d="m64 86 67-38 66 38-67 38Z"/><path class="model-face face-front" d="M64 86v93l66 37v-92Z"/><path class="model-face face-side" d="M130 124v92l67-37V86Z"/><text x="80" y="232">OBJECT</text><path class="projection-line" d="M64 86h291m66 0H131m-67 93h291m66 0h-291"/><path class="detail" d="M370 86v93h-15V86Z"/><text x="376" y="109">FRONT</text><path class="projection-line accent-line" d="M231 63h66m-66 22h66m-66 22h66"/><text x="221" y="47">PARALLEL PROJECTORS</text><path class="detail" d="M343 80v106"/><path class="detail" d="M338 83h10m-10 100h10"/><text x="324" y="202">90°</text></svg>`, 'Every projector is parallel. The view is true to the face because the picture plane is perpendicular to the viewing direction.')}
    <h2>From one face to one view</h2><p>Repeat the same process from above and from the side. The resulting plan and side views line up with the front view, so widths, heights and depths can be compared directly.</p><div class="callout warm"><strong>Remember the viewing direction</strong>The view name describes where you are looking from: front elevation from the front, plan from above, and side elevation from the side.</div>`;
  return shell(pages['how-works'], body) + endLinks('how-works');
}

function howManyPage() {
  const controls = `<span class="control-label">Show views</span><div class="segmented-control" role="group" aria-label="Choose the number of views"><button type="button" data-view-count="1" aria-pressed="false">1 view</button><button type="button" data-view-count="2" aria-pressed="false">2 views</button><button type="button" data-view-count="3" aria-pressed="true">3 views</button></div><span class="diagram-note" id="view-count-note">Three views describe width, height and depth.</span>`;
  const body = `<p class="lead-copy">A single view can hide important information. A circle might be a hole, a cylinder or a flat disk. Additional views remove that uncertainty by showing the object from other directions.</p>${diagramCard('Choose enough views to describe the part', `<div id="view-count-diagram">${projectionSvg('third', {showHidden:false})}</div>`, 'Select one, two or three views. Notice what each view contributes.', controls)}<h2>Three principal views</h2><p>Most simple objects can be described with a front view, a plan and one side view. Add another view when the shape needs it; omit views that add no new information.</p><ul><li><strong>Front elevation:</strong> height and width.</li><li><strong>Plan:</strong> width and depth.</li><li><strong>Side elevation:</strong> height and depth.</li></ul><div class="callout"><strong>Ask yourself</strong>Could someone make this object from the views shown? If a shape or feature is still ambiguous, add a view or a section.</div>`;
  return shell(pages['how-many'], body) + endLinks('how-many');
}

function anglePage(angle) {
  const isThird = angle === 'third';
  const controls = `<span class="control-label">Compare layout</span><div class="segmented-control" role="group" aria-label="Choose projection method"><button type="button" data-angle="first" aria-pressed="${!isThird}">First angle</button><button type="button" data-angle="third" aria-pressed="${isThird}">Third angle</button></div><button type="button" class="small-button" data-action="unfold">Play view-folding animation</button><span class="diagram-note" id="angle-note">${isThird ? 'Plan above; right view to the right.' : 'Plan below; right view to the left.'}</span>`;
  const body = `<p class="lead-copy">In ${isThird ? 'third-angle' : 'first-angle'} projection, a solid object is imagined in one of the four quadrants formed by the horizontal and vertical planes. Folding those planes flat places each view in a standard position around the front view.</p>${diagramCard(`${isThird ? 'Third' : 'First'}-angle view arrangement`, projectionSvg(angle), 'Use the switch to compare both conventions. The object and its views stay the same; their positions change.', controls)}<h2>Where the name comes from</h2><p>${isThird ? 'The object is placed in the third quadrant, below the horizontal plane and behind the vertical plane.' : 'The object is placed in the first quadrant, above the horizontal plane and in front of the vertical plane.'} The chosen quadrant determines which side of the front view each projected view occupies.</p><div class="callout"><strong>Check the drawing symbol</strong>First-angle and third-angle projection show the same object from the same directions. They arrange the plan and side views differently, so always identify the method before reading a drawing.</div><h2>Compare the view positions</h2><ul><li><strong>Third angle:</strong> the plan sits above the front view; the right-side view sits to its right.</li><li><strong>First angle:</strong> the plan sits below the front view; the right-side view sits to its left.</li></ul>`;
  return shell(pages[isThird ? 'third-angle' : 'first-angle'], body) + endLinks(isThird ? 'third-angle' : 'first-angle');
}

function symbolsPage() {
  const body = `<p class="lead-copy">A small truncated cone marks the projection convention used on a drawing. The circular end view and the cone side view switch sides between the two symbols.</p><div class="topic-grid"><div class="topic-card"><span class="topic-index">SYMBOL A</span><h3>First-angle projection</h3><div class="mini-symbol"><svg viewBox="0 0 220 90" role="img" aria-label="First-angle projection symbol"><path d="M19 26 87 37v25L19 73Z" fill="none" stroke="#476b65" stroke-width="2"/><ellipse cx="20" cy="49.5" rx="5" ry="23.5" fill="none" stroke="#476b65" stroke-width="2"/><circle cx="159" cy="50" r="25" fill="none" stroke="#476b65" stroke-width="2"/><circle cx="159" cy="50" r="10" fill="none" stroke="#476b65" stroke-width="1.6"/><path d="M134 50h50m-25-25v50" stroke="#94aaa0" stroke-dasharray="3 3"/></svg></div><p>The cone side view sits left of the concentric circles. The plan and right-side views fold to the opposite sides of their planes.</p></div><div class="topic-card"><span class="topic-index">SYMBOL B</span><h3>Third-angle projection</h3><div class="mini-symbol"><svg viewBox="0 0 220 90" role="img" aria-label="Third-angle projection symbol"><circle cx="58" cy="50" r="25" fill="none" stroke="#476b65" stroke-width="2"/><circle cx="58" cy="50" r="10" fill="none" stroke="#476b65" stroke-width="1.6"/><path d="M33 50h50M58 25v50" stroke="#94aaa0" stroke-dasharray="3 3"/><path d="m123 26 68 11v25l-68 11Z" fill="none" stroke="#476b65" stroke-width="2"/><ellipse cx="191" cy="49.5" rx="5" ry="23.5" fill="none" stroke="#476b65" stroke-width="2"/></svg></div><p>The concentric circles sit left of the cone side view. This is the arrangement used in the third-angle lesson.</p></div></div><h2>Read the symbol, then read the views</h2><p>Do not guess from the appearance of the object. Find the projection symbol in the title block, then use its convention to locate the plan and side views.</p><div class="callout warm"><strong>Drawing room check</strong>The two symbols use a cone and its end view. Which side the circular view appears on tells you which projection convention is in use.</div>`;
  return shell(pages['projection-symbols'], body) + endLinks('projection-symbols');
}

function hiddenLinesPage() {
  const controls = `<span class="control-label">Hidden edges</span><span class="toggle-copy"><strong id="hidden-toggle-label">Shown as dashed lines</strong></span><button class="switch" type="button" role="switch" aria-checked="true" aria-label="Show hidden edges" data-action="hidden-toggle"></button><span class="diagram-note">Toggle the rear edges on and off.</span>`;
  const body = `<p class="lead-copy">A visible edge is drawn with a continuous line. An edge that lies behind a surface can still matter, so we show it with a thin dashed line.</p>${diagramCard('Visible outline and hidden detail', projectionSvg('third'), 'Dashed edges communicate features that are not visible from this direction.', controls)}<h2>Line weight makes a difference</h2><p>Use a heavier continuous line for visible outlines and a lighter dashed line for hidden edges. If a hidden edge meets a visible outline, leave a small gap so the heavier line remains distinct.</p><div class="callout"><strong>Too many hidden lines?</strong>When hidden detail makes a view crowded, use a section view to show the interior more directly.</div>`;
  return shell(pages['hidden-lines'], body) + endLinks('hidden-lines');
}

function sectionsPage() {
  const controls = `<span class="control-label">Cut away the front half</span><span class="toggle-copy"><strong id="section-toggle-label">Section view off</strong></span><button class="switch" type="button" role="switch" aria-checked="false" aria-label="Show the section view" data-action="section-toggle"></button>`;
  const body = `<p class="lead-copy">A section is an imaginary cut through an object. Remove the material between you and the cutting plane, then draw the shape you can see inside.</p>${diagramCard('Reveal the interior with a section', `<svg class="projection-svg" viewBox="0 0 560 250" role="img" aria-label="A block with an internal bore and a cutaway section view"><text x="75" y="28">WHOLE OBJECT</text><text x="347" y="28">SECTION A–A</text><path class="model-face face-top" d="m54 83 75-42 80 43-76 44Z"/><path class="model-face face-front" d="M54 83v112l79 44v-111Z"/><path class="model-face face-side" d="M133 127v112l76-43V84Z"/><path class="detail" d="M92 105v62m75-85v63m-75 19 38 21"/><path class="hidden-edge" d="M92 105h75m-75 62h75"/><path class="detail accent-line" d="M120 65v158m-7-151 7-9 7 9m-14 145 7 9 7-9"/><text x="98" y="58">A</text><text x="130" y="58">A</text><g id="section-reveal" style="opacity:0;transition:opacity .25s"><path class="view" d="M327 52h174v164H327Z"/><path class="detail" d="M327 164h174v52H327Z"/><path d="M352 164a30 30 0 0 1 60 0v52h-60Z" fill="#e8d4ae" stroke="#54746f" stroke-width="1.2"/><path class="detail" d="M352 191h60"/><path d="M327 164h25m60 0h89" stroke="#476b65" stroke-width="2"/><text x="373" y="144">CUT SURFACE</text><text x="379" y="235">HATCHED MATERIAL</text></g></svg>`, 'The cut reveals an internal feature that would otherwise require several hidden lines.', controls)}<h2>Hatching marks the cut material</h2><p>Use thin, evenly spaced hatch lines—often at 45 degrees—to show where the cutting plane passes through solid material. Leave holes and empty spaces unhatched.</p><div class="callout"><strong>Show the cutting plane</strong>A section line with arrows marks where the imaginary cut is made and the direction you are looking.</div>`;
  return shell(pages.sections, body) + endLinks('sections');
}

function quizPage() {
  const questions = [
    ['q1', 'What describes orthographic projection?', ['A perspective image with converging edges', 'Several flat views made with parallel projectors perpendicular to the view plane', 'A shaded 3D model with no measurements'], 1],
    ['q2', 'Why might one view be insufficient?', ['It may not show the object’s depth or distinguish different forms', 'It cannot show a visible edge', 'A drawing must always contain six views'], 0],
    ['q3', 'In third-angle projection, where does the plan go?', ['Below the front view', 'Above the front view', 'To the left of the front view'], 1],
    ['q4', 'How is a hidden edge normally shown?', ['A thick continuous line', 'A thin dashed line', 'A shaded band'], 1],
    ['q5', 'What can help when many hidden lines crowd a drawing?', ['Remove all side views', 'Use a section view', 'Make every line heavier'], 1],
    ['q6', 'What identifies the projection convention?', ['The number of views', 'The title of the object', 'The projection symbol'], 2]
  ];
  const body = `<p class="lead-copy">Choose one answer for each question, then check your work. The feedback explains the drawing principle behind each answer.</p><form id="module-quiz" class="quiz">${questions.map(([id, prompt, options]) => `<fieldset class="quiz-question"><legend>${prompt}</legend>${options.map((option, index) => `<label><input type="radio" name="${id}" value="${index}" /> <span>${option}</span></label>`).join('')}</fieldset>`).join('')}<button class="primary-button" type="submit">Check answers <span class="arrow">→</span></button><span class="quiz-score" id="quiz-score" aria-live="polite"></span><p class="quiz-feedback" id="quiz-feedback" aria-live="polite"></p></form><div class="callout"><strong>Keep practising</strong>Return to any lesson from the menu to review a view layout, line type or section.</div>`;
  return shell(pages.quiz, body) + endLinks('quiz');
}

function endLinks(id) {
  if (id === 'home') return `<div class="lesson-end">${pageLink('what-is', '<small>Start the module</small>What is orthographic projection? →', 'next-link')}</div>`;
  const index = lessonOrder.indexOf(id);
  const prev = index > 0 ? lessonOrder[index - 1] : 'home';
  const next = index >= 0 && index < lessonOrder.length - 1 ? lessonOrder[index + 1] : null;
  return `<div class="lesson-end">${pageLink(prev, `<small>Previous lesson</small>← ${pages[prev].title}`, '')}${next ? pageLink(next, `<small>Next lesson</small>${pages[next].title} →`, 'next-link') : pageLink('home', '<small>Module complete</small>Return to module home ↗', 'next-link')}</div>`;
}

function readCompleted() {
  try { const stored = JSON.parse(localStorage.getItem(progressKey) || '[]'); return Array.isArray(stored) ? stored : []; } catch { return []; }
}

function updateProgress() {
  const completed = readCompleted();
  const count = lessonOrder.filter(id => completed.includes(id)).length;
  document.getElementById('progress-copy').textContent = `${count} / ${lessonOrder.length}`;
  document.getElementById('progress-bar').style.width = `${Math.round(count / lessonOrder.length * 100)}%`;
  document.querySelectorAll('.nav-child').forEach(link => {
    const visited = completed.includes(link.dataset.page);
    link.classList.toggle('visited', visited);
    link.setAttribute('data-visited', visited ? 'true' : 'false');
  });
}

function setPage(id, updateHistory = true) {
  if (!pages[id]) id = 'home';
  currentPage = id;
  if (updateHistory) history.pushState({ page: id }, '', id === 'home' ? location.pathname : `?page=${id}`);
  const page = pages[id];
  document.title = `${page.title} — Orthographic Projection`;
  document.getElementById('page-content').innerHTML = page.render();
  document.getElementById('breadcrumbs').innerHTML = id === 'home'
    ? '<span class="current">Module home</span>'
    : `${pageLink('home', 'Module home')}<span class="crumb-sep">/</span><span>${page.section}</span><span class="crumb-sep">/</span><span class="current">${page.title}</span>`;
  document.querySelectorAll('.nav-home,.nav-child').forEach(link => link.classList.toggle('active', link.dataset.page === id));
  document.querySelectorAll('.nav-group').forEach(group => {
    const active = group.querySelector(`[data-page="${id}"]`);
    group.classList.remove('is-open');
    group.classList.toggle('current-group', Boolean(active));
    group.querySelector('.nav-group-button')?.setAttribute('aria-expanded', 'false');
  });
  if (id !== 'home') {
    try { const completed = readCompleted(); if (!completed.includes(id)) localStorage.setItem(progressKey, JSON.stringify([...completed, id])); } catch { /* progress is optional when storage is disabled */ }
  }
  updateProgress();
  document.querySelector('.sidebar').classList.remove('mobile-open');
  document.querySelector('.mobile-menu-button').setAttribute('aria-expanded', 'false');
  window.scrollTo({ top: 0, behavior: 'smooth' });
  bindPageControls();
}

function bindPageControls() {
  document.querySelectorAll('[data-angle]').forEach(button => button.addEventListener('click', () => {
    const angle = button.dataset.angle;
    const figure = document.querySelector('.lesson-figure');
    const svgHost = figure?.querySelector('.projection-svg');
    if (svgHost) svgHost.outerHTML = projectionSvg(angle, { unfolded: document.querySelector('.view-layout')?.classList.contains('unfolded') });
    document.querySelectorAll('[data-angle]').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    const note = document.getElementById('angle-note');
    if (note) note.textContent = angle === 'third' ? 'Plan above; right view to the right.' : 'Plan below; right view to the left.';
    const title = document.querySelector('.figure-head strong');
    if (title) title.textContent = `${angle === 'third' ? 'Third' : 'First'}-angle view arrangement`;
    const caption = document.querySelector('.figure-caption');
    if (caption) caption.textContent = `${angle === 'third' ? 'Third' : 'First'}-angle layout selected. Use the switch to compare both conventions. The object and its views stay the same; their positions change.`;
    const fold = document.querySelector('[data-action="unfold"]');
    if (fold) fold.textContent = angle === 'third' ? 'Unfold the views' : 'Fold the views';
  }));
  document.querySelector('[data-action="unfold"]')?.addEventListener('click', event => {
    const layout = document.querySelector('.view-layout');
    const svg = layout?.closest('svg');
    const isThird = svg?.dataset.angle === 'third';
    const plan = layout?.querySelector('[data-view-name="plan"]');
    const side = layout?.querySelector('[data-view-name="side"]');
    if (plan && side && plan.animate) {
      plan.animate([{ transform: `translate(${isThird ? 0 : 34}px, ${isThird ? 84 : -97}px)` }, { transform: `translate(${isThird ? 0 : 34}px, 0px)` }], { duration: 700, easing: 'cubic-bezier(.2,.7,.2,1)' });
      side.animate([{ transform: `translateX(${isThird ? -145 : 114}px)` }, { transform: 'translateX(0)' }], { duration: 700, easing: 'cubic-bezier(.2,.7,.2,1)' });
      event.currentTarget.textContent = 'Replay view-folding animation';
    }
  });
  document.querySelector('[data-action="hidden-toggle"]')?.addEventListener('click', event => {
    const on = event.currentTarget.getAttribute('aria-checked') !== 'true';
    event.currentTarget.setAttribute('aria-checked', String(on));
    document.querySelectorAll('.hidden-edge').forEach(line => line.style.opacity = on ? '1' : '0');
    document.getElementById('hidden-toggle-label').textContent = on ? 'Shown as dashed lines' : 'Hidden edges off';
  });
  document.querySelector('[data-action="section-toggle"]')?.addEventListener('click', event => {
    const on = event.currentTarget.getAttribute('aria-checked') !== 'true';
    event.currentTarget.setAttribute('aria-checked', String(on));
    document.getElementById('section-reveal').style.opacity = on ? '1' : '0';
    document.getElementById('section-toggle-label').textContent = on ? 'Section view shown' : 'Section view off';
  });
  document.querySelectorAll('[data-view-count]').forEach(button => button.addEventListener('click', () => {
    const count = Number(button.dataset.viewCount);
    document.querySelectorAll('[data-view-count]').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    const host = document.getElementById('view-count-diagram');
    const notes = { 1: 'One view leaves depth or form ambiguous.', 2: 'Two views add depth, but a third can clarify shape.', 3: 'Three views describe width, height and depth.' };
    document.getElementById('view-count-note').textContent = notes[count];
    host?.querySelectorAll('[data-view-name]').forEach(view => {
      const visible = view.dataset.viewName === 'front' || (count >= 2 && view.dataset.viewName === 'plan') || (count >= 3 && view.dataset.viewName === 'side');
      view.style.opacity = visible ? '1' : '0.12';
    });
  }));
  document.getElementById('module-quiz')?.addEventListener('submit', event => {
    event.preventDefault();
    const answers = { q1: 1, q2: 0, q3: 1, q4: 1, q5: 1, q6: 2 };
    const form = event.currentTarget;
    const answered = Object.keys(answers).every(name => form.querySelector(`input[name="${name}"]:checked`));
    const feedback = document.getElementById('quiz-feedback');
    if (!answered) {
      feedback.className = 'quiz-feedback try-again';
      feedback.textContent = 'Answer all six questions to see your score.';
      document.getElementById('quiz-score').textContent = '';
      return;
    }
    const correct = Object.entries(answers).filter(([name, answer]) => Number(form.querySelector(`input[name="${name}"]:checked`).value) === answer).length;
    document.getElementById('quiz-score').textContent = `${correct} / 6 correct`;
    feedback.className = `quiz-feedback ${correct >= 5 ? 'correct' : 'try-again'}`;
    feedback.textContent = correct === 6 ? 'Excellent. You have the core drawing conventions down.' : correct >= 4 ? 'Good work. Revisit any lesson that still feels uncertain.' : 'Review the marked topics in the module, then give it another try.';
  });
}

renderNavigation();
const initialPage = new URLSearchParams(location.search).get('page') || 'home';
setPage(initialPage, false);

document.addEventListener('click', event => {
  const link = event.target.closest('a[data-page]');
  if (link) {
    event.preventDefault();
    setPage(link.dataset.page);
    return;
  }
  const groupButton = event.target.closest('.nav-group-button');
  if (groupButton) {
    const group = groupButton.closest('.nav-group');
    const open = group.classList.toggle('is-open');
    groupButton.setAttribute('aria-expanded', String(open));
  }
});
document.querySelector('.mobile-menu-button').addEventListener('click', event => {
  const sidebar = document.querySelector('.sidebar');
  const open = sidebar.classList.toggle('mobile-open');
  event.currentTarget.setAttribute('aria-expanded', String(open));
});
window.addEventListener('popstate', () => setPage(new URLSearchParams(location.search).get('page') || 'home', false));
