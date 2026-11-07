// What kind of thing something is, as an icon and a soft tint (tint-0..4 in app.css). Shared by the pages so a
// video format or a kind of merch looks the same everywhere.

// ---- the weekly video plan's formats ----
const IDEA = { money: 'coins', 'answer a fan': 'chatDots', news: 'megaphone', clinic: 'lightstick', proof: 'stock' }
export function ideaIcon(format) {
  return IDEA[(format || '').toLowerCase()] || 'videos'
}

// ---- TikTok formats (Videos, results) ----
const FORMATS = [
  [/pre-order|announcement/i, 'megaphone', 'GO posts'],
  [/concert|idol|fan moment/i, 'mic', 'Idol moments'],
  [/product|showcase|generic sell/i, 'bag', 'Product'],
  [/arrival|onhand|restock/i, 'stock', 'Arrivals'],
  [/seller life|behind/i, 'store', 'Behind the scenes'],
  [/lightstick/i, 'lightstick', 'Lightstick how-to'],
  [/sale|promo|giveaway/i, 'tag', 'Promos'],
  [/fan content|edit|meme/i, 'heart', 'Fan edits'],
  [/pack/i, 'stock', 'Packing'],
]
export function formatOf(f) {
  for (const [re, icon, label] of FORMATS) if (re.test(f || '')) return { icon, label }
  return { icon: 'sparkle', label: 'Other' }
}

// ---- stock items ----
const ITEMS = [
  [/id ?card/i, 'idCard'], [/card ?holder|pc ?holder/i, 'holder'], [/photo ?card|\bpc\b|photocard/i, 'photocard'],
  [/back ?pack/i, 'backpack'], [/cushion|pillow/i, 'cushion'], [/light ?stick|bong|army ?bomb|\bls\b/i, 'lightstick'],
  [/plush|doll|key ?ring|key ?chain/i, 'plush'], [/pouch/i, 'pouch'], [/bag|tote/i, 'handbag'],
  [/picket/i, 'picket'], [/slogan|banner|towel/i, 'slogan'], [/sticker/i, 'sticker'], [/badge|button|pin\b/i, 'badge'],
  [/shirt|tee|hoodie/i, 'tshirt'], [/capsule|random/i, 'gift'], [/season|calendar|diary/i, 'calDots'],
  [/album|vinyl|\blp\b|\bver\b|set|weverse|cd\b/i, 'album'], [/photo|poster|image/i, 'images'],
]
export function itemIcon(name) {
  for (const [re, icon] of ITEMS) if (re.test(name || '')) return icon
  return 'stock'
}
// a colour per kind of merch, so a page of stock reads as lightsticks / photocards / plushies, not a wall of yellow
const ITEM_TINT = { lightstick: '1', album: '1', photocard: '4', holder: '4', picket: '4', slogan: '4', idCard: '4',
  plush: '3', cushion: '3', badge: '3', sticker: '3', gift: '3', pouch: '2', handbag: '2', backpack: '2', tshirt: '2' }
export const itemTint = (name) => ITEM_TINT[itemIcon(name)] || '0'

// ---- buyers ----
// A steady tint per username, so the same buyer always looks the same.
export function tintOf(name) {
  let h = 0
  for (const c of (name || '').toLowerCase().replace(/^@/, '')) h = (h * 31 + c.charCodeAt(0)) >>> 0
  return h % 5
}
