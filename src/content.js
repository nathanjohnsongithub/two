// Everything personal lives in this file. Edit the words, maps and photos
// here; you shouldn't need to touch the game code to change the story.

export const CONFIG = {
  title: "Year Two",
  subtitle: "Nathan & Hannah",
  herName: "Hannah",
  noteLabel: "A NOTE FROM NATHAN",
};

// Shown on a letter before chapter 1.
export const PROLOGUE = [
  "Hannah,",
  "I hid some notes in a few of our favorite memories from this year.",
  "Follow them, and they'll lead you to me.",
  "- Nathan",
];

// Map legend (every row in a map must be the same length):
//   Floors (walkable) are set per area in `floors`, e.g. { ".": "wood" }
//   #  wall (tile set by `wall`)   w  window         H  hedge
//   D  exit door                   P  Hannah starts  N  character (in order from `npcs`)
//   1-9  notes (the number picks the entry in `notes`)
//   " " empty space outside the map
//   c counter   k sink    s stove    f fridge    T table     h chair
//   O stove with dinner still cooking (it steams)
//   X candlelit table     Z table with an empty dumpling plate
//   ( C )  couch (left, middle, right)    B / b  bed (top / bottom)
//   u tub   t toilet   L washer   v tv   p plant   j nightstand
//   Y tree  n bench    ~ water    l lantern   S storefront   e lamppost   * flower bed
//   W stone window     d stone door (two side by side make one big door)
//   G chair with a graduation cap    ^ roof (its bottom row gets eaves)   I brick wall with a window
//   U U-Haul (2 wide, 3 tall, cab at the bottom)   Q dumpster   F fire escape
//   x box to carry into the U-Haul                 r railing    K city skyline
//   o string lights    E elevator
//
// A chapter can add its own characters, or change what one means, in `objects`
// (e.g. { A: "taxi" }), using the tile names from tools/tiles.py. Pieces that
// join up (beds, the taxi, the dumpling house, the bar) go side by side; tall
// windows and parked cars go two high.
//
// Photos go in public/photos/ and are referenced as "/photos/name.jpg".
// Leave `photo: null` to show a placeholder until you add one.

export const AREAS = [
  {
    chapter: "Chapter 1",
    name: "Valentine's Day",
    background: "#1a1420",
    wall: "wall",
    door: "door",
    floors: {
      ".": "wood", ",": "kitchen", ":": "rug", "'": "woodPetals",
      ";": "rugBlue", '"': "rugCream", "=": "rugRunner", _: "bathTile",
    },
    // Characters for this chapter only: the chalkboard menu by the door, a
    // desk (M) with its chair (a), dresser, bookshelf, floor lamp, coffee
    // table, bathroom sink, shower (two tall), trash can and coat rack.
    objects: {
      m: "menuBoard", M: "desk", a: "deskChair", R: "dresser", g: "bookshelf", i: "floorLamp",
      J: "coffeeTable", V: "vanity", q: "shower", z: "trashCan", y: "coatRack",
    },
    intro: ["February 14th. 1055 W Pratt, apartment 2A.", "Something smells amazing... but where's Nathan?"],
    map: [
      "##ww##ww###ww#w####www####w###ww#w##",
      "#p.gg...p#RBBjMp#pM.jBBR#tVu#pRjBBM#",
      "#........#.bb.a.#.a..bb.#___#...bba#",
      "w..hXh...#.;;;..#...\"\"\".#___#..;;;.#",
      "w...''...#.;;;1.#...\"\"\".###.#..;3;.#",
      "#....''..#.;;;..#...\"\"\".##..#..;;;.#",
      "#.....'..#......#.......##.........#",
      "w......'.####.####.#######..########",
      "w.i(C).'.....................fccOck#",
      "#.(:::..'......................\"\"\"c#",
      "#.C:J:.m.'P##########.###.........c#",
      "w.):::..y#D#      #tV__q#.........z#",
      "wp..v....#        #_2__q#ccc.......#",
      "##########       ############D##ww##",
    ],
    notes: [
      {
        title: "Apartment 2A",
        caption: "My old place on Pratt, a block from the lake. The kitchen was small, but it worked.",
        photo: null,
      },
      {
        title: "Valentine's Day",
        caption: "I wanted to cook you something fancy, so I turned my apartment into a restaurant for the night.",
        photo: null,
      },
      {
        title: "The menu",
        caption: "Carbonara (your favorite), steak, and a warm sticky date cake with ice cream on top.",
        photo: null,
      },
    ],
    npcs: [],
    // One-time lines when she walks up to a tile.
    details: {
      O: ["Carbonara in the pot, steak in the pan. It's all still warm.", "Nathan was just here..."],
    },
    // Walking up to this tile once every note is found plays the goal, then
    // the exit opens.
    goal: {
      tile: "X",
      locked: ["The table is set for two... but Nathan isn't here. Maybe look around first."],
      lines: ["The table is set for two. The candles are still lit.", "No Nathan... but he left the menu."],
      cards: [
        { label: "FIRST COURSE", title: "Carbonara", caption: "Your favorite.", photo: null },
        { label: "MAIN COURSE", title: "Steak", caption: "Cooked just right (I hope).", photo: null },
        {
          label: "DESSERT",
          title: "Sticky date cake",
          caption: "Warm, with ice cream melting on top.",
          photo: null,
        },
      ],
      end: ["Dinner's still warm. He can't have gone far.", "(The front door is open.)"],
    },
  },
  {
    chapter: "Chapter 2",
    name: "Chinatown, NYC",
    background: "#1a1420",
    wall: "brick",
    door: "subway",
    floors: { ":": "sidewalk", ";": "road", "-": "roadLine", "=": "crosswalk", _: "terracotta", ",": "pavers" },
    // Characters for this chapter only.
    objects: {
      // Canal Street: taxis both ways.
      A: "taxi", a: "taxiEast",
      // The Chinatown gate: a green tile roof (Q) over a signboard (q), on two red pillars (!),
      // with a stone lion on each side (< >).
      Q: "gateRoof", q: "gateBeam", "!": "gatePillar", "<": "lionL", ">": "lionR",
      // Buildings: fire escapes, vertical signs, green pagoda roofs (^, a row of them joins up).
      F: "fireEscapeFront", k: "brickSign", "^": "pagoda",
      // Shops: red, jade, market, roast ducks, bakery, bubble tea, herbs, and the dumpling house.
      R: "shopRed", J: "shopJade", M: "shopMarket", K: "shopDucks", B: "shopBakery", T: "shopTea", H: "shopHerbs",
      V: "restaurant",
      // The street: fruit and fish stands, a steamed bun cart, pagoda phone booths, red lampposts,
      // strings of lanterns overhead.
      g: "fruitStand", f: "fishStand", z: "streetCart", b: "phoneBooth", e: "lamppostRed", i: "lanterns",
      // The park: xiangqi tables. And tables on the dumpling house patio.
      c: "chessTable", t: "table",
    },
    intro: ["Chinatown, New York City.", "Nathan has to be around here somewhere."],
    map: [
      "#IIkIFFI^^^^^^IIFFIkIII#",
      "#IIkIFFIIkIIkIIIFFIkIII#",
      "#RKMJTBRMHJBRKJTMBRJKHB#",
      "::g::f::b:::P::::g::f:::",
      ";;;AA;;;;;====;;;;;;;;;;",
      "----------====----------",
      ";;;;;;;;;;====;;;;aa;;;;",
      "::e:::::::::::::::::e:::",
      "#IIFFIkIQQQQQQQQIkIIFFI#",
      "#IkFFIIIqqqqqqqqIIIFFkI#",
      "#RKJMBTR!::::::!HJMKRBT#",
      "::g:N:f:<::::::>::f::g::",
      "iiiiiiiiiiiiiiiiiiiiiiii",
      ":b:::1::::z:::::::::b:::",
      "::::::::::::::::::::::::",
      "#^^^^^^IkI::IkFF^^^^^^I#",
      "#IIkIFFIkI::IkFFIIkIIFI#",
      "#IkIIFFIIk::IIFFkIIIkFI#",
      "#BRHKTJMRB::JKTRMHBRJKT#",
      ":::g:f:::::::::::g::f:::",
      "iiiiiiiiiiiiiiiiiiiiiiii",
      "::::::b:::::::2:::z:::::",
      "::::::::::::::::::::::::",
      "#IkFFI::IIkFF^^^^^^^^^I#",
      "#IIFFk::IkFFIIIkIIIkIIF#",
      "#kIFFI::IIFFkIFFIkIFFIF#",
      "#MRKBJ::TRHJBVVVVVVVVVK#",
      ":::::::::::::_________::",
      "iiiiiiiiiiiiiiiiiiiiiiii",
      "Y,,,,,Y,,,,Y:_hZh_hth_::",
      ",,cN,,,,,c,,:_________::",
      ",,,,,,,,,,,,:_hth_hth_::",
      "Y,,,,3,,,,,Y:_________::",
      ",,c,,,,,,c,,::::::::::::",
      ",,,,,,,,,,,,:e::::::::e:",
      "Y,,nn,,nn,,Y::::::D:::::",
      "########################",
    ],
    notes: [
      { title: "Chinatown", caption: "We kept finding our way back here.", photo: null },
      { title: "Every window", caption: "Roast ducks, egg tarts, bubble tea. We wanted to try all of it.", photo: null },
      { title: "Dumplings", caption: "A plate of fried dumplings, to share. That was the plan, anyway.", photo: null },
    ],
    // The auntie at the fruit stand and the uncle at the xiangqi tables (tools/local_sprite.py).
    npcs: [
      {
        name: "Auntie",
        sprite: "locals",
        frame: 0,
        lines: ["Looking for your boyfriend? Very hungry boy?", "He asked me where to get the best dumplings. I sent him down the street."],
      },
      {
        name: "Uncle",
        sprite: "locals",
        frame: 1,
        lines: ["Shh. I'm about to win.", "...Your boyfriend? He watched one game, then followed his nose to the dumpling house."],
      },
    ],
    goal: {
      tile: "Z",
      locked: ["A plate with nothing but crumbs on it. Better look around first."],
      lines: [
        "An empty plate. Just crumbs and a pair of chopsticks.",
        "There's a note tucked under it:",
        "\"Sorry. I ate all the dumplings. By accident. -N\"",
        "He was definitely here.",
      ],
      cards: [],
      end: ["(The subway is open.)"],
    },
  },
  {
    chapter: "Chapter 3",
    name: "Graduation",
    background: "#1a1420",
    // Hannah's sprite for this chapter (see tools/hannah_sprite.py).
    player: "hannah_gown",
    wall: "stone",
    door: "stoneDoor",
    floors: { ".": "grass", ",": "walkway", ";": "stage" },
    // Characters for this chapter only.
    objects: {
      e: "lamppostBanner", m: "stoneBanner", h: "foldingChair", "!": "podium", b: "balloons",
      s: "loyolaSign", q: "waterSail",
      // Madonna della Strada: copper roof with a cross, stained glass, a rose window.
      c: "roofCopper", "+": "roofCross", g: "chapelWindow", O: "roseWindow",
      // The dome on the main hall's roof.
      u: "dome",
    },
    intro: ["Loyola, Lake Shore Campus. Graduation day!", "Nathan has to be here somewhere... right?"],
    map: [
      "^^^^^^^^uu^^^^^^^^^~~~",
      "^^^^^^^^^^^^^^^^^^^~~~",
      "##W#W#WmWWmW#W#W#W#~~~",
      "##W#W#W#dd#W#W#W#W#~~~",
      "H.*****bP,b******.,~~~",
      "H.......,,.s.....e,~~~",
      "H.Y.....,,.....Y..,~~~",
      "H......e,,.Y......,~~~",
      "H....Y..,,.......2,~~~",
      "H.......,,.N......,~~~",
      "H...1...,,..cc++cc,~~~",
      "H.......,,..cccccc,~~~",
      "H..Y....,,..#g##g#,~~~",
      "H.......,,..#g##g#,~q~",
      "H.....Y.,,e.##OO##,~~~",
      "H.......,,..##dd##,~~~",
      "HY......,,..**,,**,~~~",
      "H.......,,...N,,..,~~~",
      "H....n..,,.n..,,..,~~~",
      "H,,,,,,,,,,,,,,,,,,~~~",
      "H......e,,........,~~~",
      "Hb;;;!;;,,........,~~~",
      "H.;;;;;;,,.Y....Y.,~~~",
      "H.......,,........,~~~",
      "H.hhhhhh,,........,~~~",
      "H.......,,.......N,~~~",
      "H.hhhGhh,,..Y.....,~~~",
      "H.......,,e.......,~~~",
      "H.hhhhhh,,........,~~~",
      "H.......,,...3.Y..,~~~",
      "H.......,,........,~~~",
      "H.......,,........,~~~",
      "##W#W####D###W#W#W#~~~",
      "###################~~~",
    ],
    notes: [
      { title: "We did it", caption: "Two Loyola graduates. I'm so proud of you.", photo: null },
      { title: "The lake", caption: "Of all the campuses in Chicago, ours had Lake Michigan right there.", photo: null },
      { title: "Four years", caption: "Four years of classes, and somehow the best part was you.", photo: null },
    ],
    // Classmates in cap and gown (frame picks the look in tools/grad_sprite.py).
    npcs: [
      {
        name: "Classmate",
        sprite: "grads",
        frame: 0,
        lines: ["Congrats, Hannah! Nathan? I think I saw him heading toward the chapel."],
      },
      {
        name: "Classmate",
        sprite: "grads",
        frame: 1,
        lines: ["Nathan? You JUST missed him!", "He said something about the ceremony chairs?"],
      },
      {
        name: "Classmate",
        sprite: "grads",
        frame: 2,
        lines: ["Everyone's wearing the same gown. Good luck finding anyone in this crowd."],
      },
    ],
    goal: {
      tile: "G",
      locked: ["A graduation cap left on a chair... Look around first."],
      lines: [
        "A graduation cap, left on a chair. The tassel's already turned.",
        "There's a note tucked inside:",
        "\"Congrats, graduate. So proud of you. Keep looking. -N\"",
        "Of course he's not here.",
      ],
      cards: [],
      end: ["(The door is open.)"],
    },
  },
  {
    chapter: "Chapter 4",
    name: "Moving Day",
    background: "#1a1420",
    wall: "brick",
    floors: { ".": "alley", "-": "alleyDrain", ",": "grass", ":": "sidewalk" },
    // Characters for this chapter only. The alley behind the old place: the
    // backs of the buildings (red or tan brick, fire escapes, back doors,
    // downspouts, electric meters, glass-block windows, dryer vents, shady
    // gangways between them, their back porch with stairs down to the gate),
    // yards with a grill and flower beds, garages with roll-up doors and shingle roofs
    // (two rows of roof join up), fences, gates and chain-link, blue and black
    // carts, a dumpster, trash bags, a mattress left against the fence (two
    // tall), a stray cat, power poles with the lines strung overhead, parked
    // cars (two tall) and traffic cones.
    objects: {
      F: "fireEscapeFront", b: "backDoor", p: "porch", j: "porchStairs",
      u: "brickTan", W: "brickTanWindow", d: "downspout", M: "meters", O: "glassBlock", v: "dryerVent",
      n: "backDoorTan", "|": "gangway", q: "grill",
      s: "shingles", G: "garage", f: "fence", g: "fenceGate", c: "chainLink",
      B: "cartBlue", K: "cartBlack", t: "trashBags", m: "mattress", k: "cat",
      e: "pole", w: "wires", A: "car", i: "cone",
    },
    intro: ["Moving day. Goodbye, Rogers Park.", "Carry every box to the U-Haul."],
    details: {
      k: ["A stray cat. It watches you carry boxes.", "It does not offer to help."],
    },
    map: [
      "dFF#I#|uWuud#I#I#d|#FF#I#uuWuuWu|d#I#FF#",
      "dFF#I#|uWuWdpppppd|#FF##vuuWuuuu|d###FF#",
      "dO#vMb|uunudpppppd|#O#Mb#uuunuuu|dOvM#b#",
      "sssss,,,m,,#ppjpp#ssss,,,,q,,,**ssssss,,",
      "GGGGGfgfmfffffgfffGGGGcccffgffffGGGGGGff",
      ".....B.K..KB..P.K..x..QQ..k....t......tB",
      "....x...................1.....x.........",
      "----------------------------------------",
      "...........x........................x...",
      "ww.wwwwwwwwwwwwwwww.wwwwwwwwwwwwwwwww.ww",
      "K.e.....BK.....t...e..K...iUUi...BK..e..",
      "sssss:A:ffffgfffffssssssff:UU:fffgffssss",
      "sssss:A:,,,Y,,q,,,ssssss,,:UU:**,,Y,ssss",
      ",,Y,,,,,,,,,,,,Y,,,,,,,,,,,,,,,,,,,,,Y,,",
      ",,,***,,,,,,,,,,,,,,Y,,,***,,,,Y,,,,,,,,",
    ],
    notes: [{ title: "Moving day", caption: "Goodbye Rogers Park, hello Lakeview.", photo: null }],
    npcs: [],
    goal: {
      tile: "U",
      locked: ["The U-Haul's all packed... but there's still a note around here somewhere."],
      lines: ["Everything's packed.", "Next stop: Lakeview."],
      cards: [],
      end: [],
      // Go straight to the next chapter instead of opening a door.
      advance: true,
    },
  },
  {
    chapter: "Chapter 5 · Morning",
    name: "Decker's Bagels",
    background: "#1a1420",
    wall: "brick",
    floors: { ":": "sidewalk", ";": "road", "-": "roadLine", "=": "crosswalk" },
    // Characters for this chapter only: the pop-up's sign (three wide) over its
    // window (glass, the open window, glass), the pickup table with the bag,
    // the chalkboard, a bike rack, taxis both ways.
    objects: {
      S: "deckerSign", "(": "popupWindowL", w: "popupWindowM", ")": "popupWindowR",
      X: "pickupTable", m: "bagelMenu", k: "bikeRack", F: "fireEscapeFront", A: "taxi", a: "taxiEast",
    },
    intro: ["The last date before your new job.", "First stop: Decker's Bagels."],
    map: [
      "##II###II###II##",
      "##II###II###II##",
      "######SSS#######",
      "##I###(w)###I###",
      ":m:::::::X:::k::",
      "::Y::N::::::::Y:",
      "::::N:::::1:::::",
      ":hTh:::::::hTh::",
      ":e::::::::::::e:",
      ";;AA;;====;;;;;;",
      "------====------",
      ";;;;;;====;;aa;;",
      ":::::::P::::::::",
      "##II###II###II##",
      "##II###II###II##",
    ],
    notes: [
      { title: "Decker's", caption: "Sourdough bagels from a pop-up window. The last date before your first day started here.", photo: null },
    ],
    // Two people in line (no names, so no tags over their heads), and the
    // worker leaning out of the window (`at` puts her in the window tile
    // instead of on an N).
    npcs: [
      { sprite: "locals", frame: 3, lines: ["Worth the wait. Trust me."] },
      {
        sprite: "locals",
        frame: 4,
        lines: ["Somebody just ordered two sandwiches and took off grinning.", "Said something about dinner plans?"],
      },
      {
        name: "Decker's",
        sprite: "locals",
        frame: 2,
        at: "w",
        lines: [
          "Morning! You must be Hannah.",
          "He already ordered for you: a bacon, egg and cheese, and a chicken apple sausage and egg.",
          "It's in the bag on the table.",
        ],
      },
    ],
    details: {
      m: ["The chalkboard: bagels, schmears, sandwiches.", "All sourdough."],
    },
    goal: {
      tile: "X",
      locked: ["A paper bag with a heart drawn on it... Look around first."],
      lines: ["A paper bag with a heart drawn on it. Still warm.", "Two bagel sandwiches inside."],
      cards: [
        { label: "BREAKFAST", title: "Bacon, egg & cheese", caption: "On a sourdough bagel.", photo: null },
        { label: "BREAKFAST", title: "Chicken apple sausage & egg", caption: "On a sourdough bagel.", photo: null },
      ],
      end: ["There's a note stapled to the bag:", "\"Eat up. Dinner's in the West Loop tonight. -N\""],
      advance: true,
    },
  },
  {
    chapter: "Chapter 5 · Dinner",
    name: "Yokocho",
    background: "#1a1420",
    // Low light: a dim, warm tint, with the lanterns and lit signs glowing through it.
    tint: [28, 14, 8, 0.45],
    wall: "slatWall",
    floors: { ".": "woodDark", ",": "slate" },
    // Characters for this chapter only: sake shelves and lit box signs on the
    // slat walls, noren curtains in the doorways, the chefs' back counter (c),
    // the U-shaped hinoki counter ([ and ] are its arms, = its front, { and }
    // the corners, G your saved spot), stools, standing lit signs, lanterns.
    objects: {
      K: "sakeShelf", L: "boxSign", n: "noren", c: "prepCounter",
      "[": "hinokiL", "]": "hinokiR", "=": "hinokiFront", "{": "hinokiBL", "}": "hinokiBR", G: "hinokiSando",
      o: "stool", A: "andon", l: "lantern",
    },
    intro: ["Dinner at Yokocho, in the West Loop.", "Handrolls at the counter... and hopefully Nathan."],
    map: [
      "#KK#L##n##L#KK##",
      "#...[cccccc]...#",
      "#.l.[,,,,,,].l.#",
      "#..o[N,,,,,]o..#",
      "#...[,,,,,,]...#",
      "#..o[,,,,,N]o..#",
      "#...[,,,,,,]...#",
      "#..o[,,,,,,]o..#",
      "#.l.{==G===}.l.#",
      "#....o.o.o.....#",
      "#..............#",
      "#A.hTh....hTh.A#",
      "#......l.......#",
      "#..1...........#",
      "#......P.......#",
      "#######n########",
    ],
    notes: [
      { title: "Yokocho", caption: "Handrolls at the counter, the chefs right in front of us. Dinner before your big day.", photo: null },
    ],
    // The chefs inside the U; `reach` lets them talk to you across the counter.
    npcs: [
      {
        name: "Chef",
        sprite: "locals",
        frame: 5,
        reach: 36,
        lines: ["Irasshaimase! Welcome!", "Hannah? Your seat's saved, at the front of the counter.", "He just stepped out. He ordered you dessert."],
      },
      {
        name: "Chef",
        sprite: "locals",
        frame: 6,
        reach: 36,
        lines: ["Handrolls go straight from my hands to yours.", "Eat them right away, while the nori's still crisp."],
      },
    ],
    goal: {
      tile: "G",
      locked: ["Your seat's saved... but there's still a note around here somewhere."],
      lines: ["Two seats saved at the counter. One's empty.", "Waiting at your spot: a strawberry matcha cream sando."],
      cards: [
        { label: "DESSERT", title: "Strawberry matcha cream sando", caption: "Strawberries and matcha cream on soft milk bread.", photo: null },
      ],
      end: ["There's a note under the plate:", "\"Save room. Drinks on the roof of the Carbide & Carbon Building. -N\""],
      advance: true,
    },
  },
  {
    chapter: "Chapter 5 · Drinks",
    name: "Chateau Carbide",
    background: "#1b2340",
    // Tints the world dark blue and makes the string lights and candle glow.
    night: true,
    wall: "decoWall",
    // Characters for this chapter only: the view (V, a 14x4 block: the
    // skyline with Willis, Marina City, Trump, Wrigley, Aon and the Hancock),
    // city lights far below the railings, the bar, candlelit cafe tables,
    // patio heaters, and the DJ's booth (Q, two wide) between two speakers.
    // People sit at the tables: "a" is a seat on the left of a table, "b" on
    // the right, "m" is behind the bar, "d" behind the decks (they're all
    // deck underneath; the people come from `npcs`).
    floors: { ".": "deck", a: "deck", b: "deck", m: "deck", d: "deck" },
    objects: { V: "view", k: "cityLights", c: "bar", T: "bistroTable", H: "heater", Q: "djBooth", Z: "speaker" },
    intro: ["The rooftop of the Carbide & Carbon Building.", "Drinks after dinner, to celebrate your new job."],
    map: [
      "VVVVVVVVVVVVVV",
      "VVVVVVVVVVVVVV",
      "VVVVVVVVVVVVVV",
      "VVVVVVVVVVVVVV",
      "krrrrrrrrrrrrk",
      "krp..hXN...prk",
      "kr..........rk",
      "kroooooooooork",
      "kr.aTb..aTb.rk",
      "kr....H.....rk",
      "kr.aTb...Tb.rk",
      "kroooooooooork",
      "kr......1...rk",
      "kr..d.H..m.2rk",
      "krZQQZ..cccprk",
      "kr....P.....rk",
      "######EE######",
      "##############",
    ],
    notes: [
      { title: "Chateau Carbide", caption: "Green and gold, the whole city lit up around us.", photo: null },
      { title: "Your new job", caption: "We came up here to celebrate before your first day. I'm so proud of you.", photo: null },
    ],
    npcs: [
      { name: "Nathan", sprite: "nathan", lines: [] },
      // Guests at the tables, in map order: frames 7-10 face right (seats "a"),
      // 11-14 face left (seats "b"). Guests with no lines just enjoy the view.
      { at: "a", sprite: "locals", frame: 7, lines: ["Cheers! We're celebrating too."] },
      { at: "a", sprite: "locals", frame: 8, lines: [] },
      { at: "a", sprite: "locals", frame: 10, lines: ["You can see the whole river from up here."] },
      { at: "b", sprite: "locals", frame: 12, lines: [] },
      { at: "b", sprite: "locals", frame: 13, lines: ["That guy by the railing keeps checking the elevator.", "Friend of yours?"] },
      { at: "b", sprite: "locals", frame: 14, lines: [] },
      { at: "b", sprite: "locals", frame: 11, lines: ["Best seat in the city."] },
      {
        name: "DJ",
        at: "d",
        sprite: "locals",
        frame: 16,
        reach: 34,
        lines: ["Any requests?", "...The guy by the railing already asked for a slow one.", "Said he's waiting for someone."],
      },
      {
        name: "Bartender",
        at: "m",
        sprite: "locals",
        frame: 15,
        reach: 34,
        lines: ["What can I get you?", "Oh, you're Hannah. Your drink's already waiting at his table."],
      },
    ],
    // The goal here is Nathan himself.
    goal: {
      tile: "N",
      speaker: "Nathan",
      locked: ["Not yet! Read the rest of my notes first."],
      lines: [
        "You found me.",
        "Sorry for making you chase me through our whole year.",
        "Every note was leading you here.",
        "Happy anniversary, Hannah.",
      ],
      cards: [],
      end: [],
      advance: true,
    },
  },
];

export const ENDING = {
  letter: [
    "Two years.",
    "Write your letter here, one line per tap.",
    "Keep each line short so it fits on a phone screen.",
  ],
  giftIntro: "Your real present is...",
  gift: "Placeholder gift reveal",
  signoff: "Happy anniversary. ♥",
};
