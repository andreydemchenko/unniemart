// Icons for K-pop merch that no icon set has: lightsticks, photocards, pickets, slogans. Drawn on Phosphor's 256 grid
// in its duotone style (16-wide round strokes, a 20% fill), so they sit next to the Phosphor ones without standing out.
const S = 'fill="none" stroke="currentColor" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"'
const both = (shape) => shape.replace('/>', ' opacity="0.2"/>') + shape.replace('/>', ` ${S}/>`)

export const merch = {
  lightstick:
    both('<circle cx="128" cy="100" r="52"/>') +
    `<path d="M104,152h48v16a8,8,0,0,1-8,8H112a8,8,0,0,1-8-8Z" ${S}/>` +
    `<path d="M116,176v44a12,12,0,0,0,24,0V176" ${S}/>` +
    `<path d="M106,92a26,26,0,0,1,20-20" ${S}/>` +
    `<path d="M128,34V20M81,53,71,43M175,53l10-10" ${S}/>`,
  photocard:
    both('<rect x="60" y="24" width="136" height="208" rx="16"/>') +
    `<circle cx="128" cy="100" r="28" ${S}/>` +
    `<path d="M84,184c8-24,25-36,44-36s36,12,44,36" ${S}/>`,
  album:
    `<path d="M184,60.1A72,72,0,0,1,184,195.9" ${S}/>` +
    both('<rect x="32" y="52" width="152" height="152" rx="8"/>') +
    `<circle cx="108" cy="128" r="28" ${S}/>`,
  badge:
    both('<circle cx="128" cy="128" r="96"/>') +
    `<path d="M128,170s-44-24-44-54a22,22,0,0,1,44-6,22,22,0,0,1,44,6C172,146,128,170,128,170Z" ${S}/>` +
    `<path d="M166,62a80,80,0,0,1,28,28" ${S}/>`,
  picket:
    both('<rect x="40" y="24" width="176" height="124" rx="12"/>') +
    `<path d="M128,148v84" ${S}/>` +
    `<path d="M128,112s-30-16-30-36a15,15,0,0,1,30-4,15,15,0,0,1,30,4C158,96,128,112,128,112Z" ${S}/>`,
  slogan:
    both('<rect x="16" y="80" width="224" height="96" rx="12"/>') +
    `<path d="M56,116H200M88,144h80" ${S}/>`,
  plush:
    both('<circle cx="128" cy="144" r="68"/>') +
    `<path d="M66.8,114.4A26,26,0,1,1,103.4,80.6M152.6,80.6a26,26,0,1,1,36.6,33.8" ${S}/>` +
    '<circle cx="104" cy="136" r="10"/><circle cx="152" cy="136" r="10"/>' +
    `<path d="M116,170q12,10,24,0" ${S}/>` +
    `<circle cx="128" cy="44" r="16" ${S}/><path d="M128,60V76" ${S}/>`,
  pouch:
    both('<path d="M56,80H200a16,16,0,0,1,16,14l12,96a16,16,0,0,1-16,18H44a16,16,0,0,1-16-18L40,94A16,16,0,0,1,56,80Z"/>') +
    `<path d="M48,112H208" ${S}/>` +
    `<path d="M168,112v22" ${S}/><rect x="158" y="134" width="20" height="28" rx="8" ${S}/>`,
  holder:
    both('<rect x="60" y="64" width="136" height="168" rx="20"/>') +
    `<rect x="84" y="90" width="88" height="116" rx="8" ${S}/>` +
    `<path d="M128,172s-26-14-26-32a13,13,0,0,1,26-4,13,13,0,0,1,26,4C154,158,128,172,128,172Z" ${S}/>` +
    `<circle cx="128" cy="32" r="16" ${S}/><path d="M128,48V64" ${S}/>`,
  cushion:
    both('<path d="M56,56C104,40,152,40,200,56c16,48,16,96,0,144-48,16-96,16-144,0C40,152,40,104,56,56Z"/>') +
    '<circle cx="100" cy="116" r="10"/><circle cx="156" cy="116" r="10"/>' +
    `<path d="M104,156q24,20,48,0" ${S}/>`,
}
