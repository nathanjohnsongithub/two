// Everything personal lives in this file. Edit the words, maps and photos
// here; you shouldn't need to touch the game code to change the story.

export const CONFIG = {
  title: "Year Two",
  subtitle: " Hannah & Nathan",
  herName: "Hannah",
  noteLabel: "A NOTE FROM NATHAN",
  // Music for the title screen and the letter (see src/music.js).
  music: "title",
};

// Shown on a letter before chapter 1.
export const PROLOGUE = [
  "Hannah!",
  "Happy two freaking years!",
  "To celebrate, I made you a little game.",
  "I hid some notes in a few of our favorite memories from this year.",
  "Follow them, and they'll lead you to me.",
  "Nathan ♡",
];

// Map legend (every row in a map must be the same length):
//   Floors (walkable) are set per area in `floors`, e.g. { ".": "wood" }
//   #  wall (tile set by `wall`)   w  window         H  hedge
//   D  exit door (two side by side make a wide one, if the door has halves)
//   P  Hannah starts  N  character (in order from `npcs`)
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
    // Evening: the apartment dims to blue, and the candles, the lamps and
    // dinner on the stove glow through it. [red, green, blue, strength]
    tint: [12, 10, 44, 0.6],
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
    // The song that plays in this chapter: a name from src/music.js, or a
    // path to an audio file in public/ (like "/music/our-song.mp3").
    music: "valentine",
    intro: ["February 14th. 1055 W Pratt, apartment 2A.", "Also known as the Pratt House.","Something smells amazing... but where's Nathan?"],
    // Right after the intro, she catches Nathan slipping away: he walks this
    // path of [column, row] map tiles (counted from 0), fades out at the end,
    // and then she says `lines`. `carry` puts a tile over his head.
    glimpse: {
      path: [[32, 9], [32, 12], [29, 12], [29, 13]],
      lines: ["Wait... was that Nathan, sneaking out the back?", "What is he up to?"],
    },
    map: [
      "##ww##ww###ww#w####www####w###ww#w##",
      "#p.gg...p#RBBjMp#pM.jBBR#tVu#pRjBBM#",
      "#........#.bb.a.#.a..bb.#___#...bba#",
      "w..hXh...#.;;;..#...\"\"\".#___#..;;;.#",
      "w...''...#.;;;1.#...\"\"\".###.#..;2;.#",
      "#....''..#.;;;..#...\"\"\".##..#..;;;.#",
      "#.....'..#......#.......##.........#",
      "w......'.####.####.#######..########",
      "w.i(C).'......''.....''......fccOck#",
      "#.(:::..''''''.'''''''.''''....\"\"\"c#",
      "#.C:J:....P##########.###..'''....c#",
      "w.):::...#D#      #tV__q#.........z#",
      "wp..v....#        #____q#ccc.......#",
      "##########        ###########D##ww##",
    ],
    notes: [
      {
        title: "Apartment 2A",
        caption: "The Pratt house right off the lake and just a block away from my LOMLs place. So many amazing memories here including the one from this night",
        photo: "photos/chapter_1/76449857-D54C-473D-AFD2-C3C7A7BA7895_1_105_c.jpeg",
      },
      {
        title: "Valentine's Day",
        caption: "I wanted to cook something special for you, and I figured cooking some of your favorite dishes would be the best way to do that.",
        photo: "photos/chapter_1/altoids.jpeg",
      },
    ],
    npcs: [],
    // One-time lines when she walks up to a tile.
    details: {
      O: ["Carbonara boiling in the water, Steak searing in the pan. It's all still warm."],
    },
    // Walking up to this tile once every note is found plays the goal, then
    // the exit opens.
    goal: {
      tile: "X",
      locked: ["The table is set for two... but Nathan isn't here. Maybe look around first."],
      lines: ["The table is set for two. The candles are still lit.", "No Nathan... but he left the menu."],
      cards: [
        { label: "MAIN COURSE", title: "Steak & Carbonara", caption: "Cooked almost as good as the one in Ohio.", photo: "public/photos/chapter_1/carbonara-steak.jpeg" },
        {
          label: "DESSERT",
          title: "Sticky date cake",
          caption: "Warm, with that ice cream melting on top. Almost as good as Trivoli Taverns",
          photo: "public/photos/chapter_1/stick_date_cake_finished.jpeg",
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
      // Parked taxis, if you want any (the ones driving are in `traffic`).
      A: "taxi", a: "taxiEast",
      // The Chinatown gate: a green tile roof (Q) over a signboard (q), on two red pillars (!),
      // with a stone lion on each side (< >).
      Q: "gateRoof", q: "gateBeam", "!": "gatePillar", "<": "lionL", ">": "lionR",
      // Buildings: red brick (# plain, I with a window), tan brick (o plain, O window),
      // brick painted jade green (w plain, W window), fire escapes, vertical signs,
      // green pagoda roofs (^, a row of them joins up).
      o: "brickTan", O: "brickTanWindow", w: "brickGreen", W: "brickGreenWindow",
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
    music: "chinatown",
    intro: ["Chinatown, New York City.", "Nathan has to be around here somewhere."],
    // Canal Street: taxis both ways along these map rows. They stop for her at
    // the crosswalk (or anywhere else she steps out).
    traffic: [
      { row: 4, car: "taxi" },
      { row: 6, car: "taxiEast" },
    ],
    // The crowd: `look` picks who (a row in tools/crowd_sprite.py). Each walks
    // their `path` of [column, row] tiles and back (or round, with `loop`), or
    // stands `at` a tile facing `face`. Add `lines` and they'll say something
    // when she walks up.
    people: [
      { look: 2, path: [[3, 7], [19, 7]] },
      { look: 4, path: [[12, 7], [12, 14], [20, 14]] },
      { look: 0, path: [[1, 14], [22, 14]] },
      { look: 1, path: [[22, 22], [2, 22]] },
      { look: 3, at: [7, 19], face: "up" },
      { look: 5, path: [[1, 31], [10, 31], [10, 34], [1, 34]], loop: true },
      { look: 15, path: [[9, 3], [16, 3]] },
      { look: 16, path: [[11, 13], [11, 22]] },
      { look: 17, path: [[7, 21], [7, 31]] },
      { look: 18, at: [17, 20], face: "up", lines: ["These lychees are a steal.", "Don't tell the auntie I said that."] },
      { look: 19, path: [[13, 34], [21, 34]] },
      { look: 20, at: [9, 31], face: "up" },
    ],
    // A few pigeons pecking around each of these tiles. They scatter when she gets close.
    pigeons: [[16, 14], [7, 22], [6, 32]],
    // Past the gate, ducking down the alley toward Pell St.
    glimpse: {
      path: [[13, 13], [13, 14], [10, 14], [10, 18]],
      lines: ["Nathan?!", "...Gone around the corner. He's fast when there's food involved."],
    },
    map: [
      "#I#kFF#w^^^^^^woOOo#IkI#",
      "#I#kFF#wWwWWwWwoOOo#IkI#",
      "#RKMJTBRMHJBRKJTMBRJKHB#",
      "::g::f::b:::P::::g::f:::",
      ";;;;;;;;;;====;;;;;;;;;;",
      "----------====----------",
      ";;;;;;;;;;====;;;;;;;;;;",
      "::e:::::::::::::::::e:::",
      "#OoOFF#kQQQQQQQQI#IwWWw#",
      "#OoOFF#kqqqqqqqqIkIwWWw#",
      "#RKJMBTR!::::::!HJMKRBT#",
      "::g:N:f:<::::::>::f::g::",
      "iiiiiiiiiiiiiiiiiiiiiiii",
      ":b:::1::::z:::::::::b:::",
      "::::::::::::::::::::::::",
      "#^^^^^^I#I::IFF#^^^^^^o#",
      "#wWwwWwIkI::IFF#oOoOoOo#",
      "#wWwwWwIkI::IFF#oOoOoOo#",
      "#BRHKTJMRB::JKTRMHBRJKT#",
      ":::g:f:::::::::::g::f:::",
      "iiiiiiiiiiiiiiiiiiiiiiii",
      "::::::b:::::::::::z:::::",
      "::::::::::::::::::::::::",
      "#oOoOo::IkFF#^^^^^^^^^##",
      "#oOoOo::IkFF#wWwwWwwWwI#",
      "#oOoOo::I#FF#wWwwWwwWwI#",
      "#MRKBJ::TRHJBVVVVVVVVVK#",
      ":::::::::::::_________::",
      "iiiiiiiiiiiiiiiiiiiiiiii",
      "Y,,,,,Y,,,,Y:_hZh_hth_::",
      ",,cN,,,,,c,,:_________::",
      ",,,,,,,,,,,,:_hth_hth_::",
      "Y,,,,,,,,,,Y:_________::",
      ",,c,,,,,,c,,::::::::::::",
      ",,,,,,,,,,,,:e::::::::e:",
      "Y,,nn,,nn,,Y::::::D:::::",
      "########################",
    ],
    notes: [
      { title: "Chinatown", caption: "It's somehow always asian, Also look at how cute we look.", photo: "public/photos/chapter_2/chinatown_selfie.jpeg" },
    ],
    // The auntie at the fruit stand and the uncle at the xiangqi tables
    // (tools/local_sprite.py). She has to talk to both before the dumpling plate.
    npcs: [
      {
        name: "Auntie",
        required: true,
        hint: "the auntie at the fruit stand",
        sprite: "locals",
        frame: 0,
        lines: ["Looking for your boyfriend? Very hungry boy?", "He asked me where to get the best dumplings. I sent him down the street."],
      },
      {
        name: "Uncle",
        required: true,
        hint: "the uncle at the xiangqi tables",
        sprite: "locals",
        frame: 1,
        lines: ["Shh. I'm about to win.", "...Your boyfriend? He watched one game, then followed his nose to the dumpling house."],
      },
    ],
    goal: {
      tile: "Z",
      locked: ["A plate with nothing but crumbs on it. Better look around first."],
      // Shown once the note is found but she hasn't talked to the auntie and the
      // uncle yet. {who} becomes whoever's left.
      lockedTalk: ["A plate with nothing but crumbs on it.", "Someone around here must have seen him. Maybe {who}?"],
      lines: [
        "An empty plate. Just crumbs and a pair of chopsticks.",
        "There's a note tucked under it:",
        "\"Sorry. My big old fatass ate all the dumplings while you were filming some HanEatsYumYum content. -Nathan\"",
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
      // A ceremony chair with someone's family in it (they come from `npcs`).
      a: "foldingChair",
      s: "loyolaSign", q: "waterSail",
      // Madonna della Strada: copper roof with a cross, stained glass, a rose window.
      c: "roofCopper", "+": "roofCross", g: "chapelWindow", O: "roseWindow",
      // The dome on the main hall's roof.
      u: "dome",
    },
    music: "graduation",
    intro: ["Loyola's Campus, Rogers Park. Graduation day!", "Nathan has to be here somewhere... right?"],
    // In his cap and gown, off into the chapel.
    glimpse: {
      sprite: "nathan_gown",
      path: [[9, 10], [9, 19], [14, 19], [14, 15]],
      lines: ["Was that Nathan, in his cap and gown?", "Everyone looks the same in these... but I'd know that walk anywhere."],
    },
    // Classmates in their gowns wandering the quad, and families.
    people: [
      { look: 6, path: [[2, 30], [17, 30]] },
      { look: 7, path: [[1, 23], [17, 23]] },
      { look: 8, path: [[18, 5], [18, 31]] },
      { look: 9, at: [3, 15], face: "right" },
      { look: 10, at: [4, 15], face: "left", lines: ["Congratulations, graduate!"] },
      { look: 11, at: [14, 22], face: "left" },
      { look: 21, path: [[8, 6], [8, 32]] },
      { look: 22, at: [13, 27], face: "left" },
      { look: 23, at: [12, 27], face: "right", lines: ["Smile! ...One more!", "...Okay, one more."] },
      { look: 24, path: [[1, 19], [17, 19]] },
    ],
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
      "H.aahhah,,........,~~~",
      "H.......,,.......N,~~~",
      "H.hahGha,,..Y.....,~~~",
      "H.......,,e.......,~~~",
      "H.hhaahh,,........,~~~",
      "H.......,,.....Y..,~~~",
      "H.......,,........,~~~",
      "H.......,,........,~~~",
      "##W#W###DD###W#W#W#~~~",
      "###################~~~",
    ],
    notes: [
      { title: "We did it", caption: "Two Loyola graduates look as us go", photo: "public/photos/chapter_3/h_and_n_grad_photo.JPG" },
      { title: "The lake", caption: "Some would say the only redeming quality about this school", photo: "public/photos/chapter_3/the_lake.jpeg" },
    ],
    // Classmates in cap and gown (frame picks the look in tools/grad_sprite.py).
    // She has to talk to all three before the cap on the chair.
    npcs: [
      {
        name: "Krisjanis",
        required: true,
        hint: "Krisjanis by the main hall",
        sprite: "grads",
        frame: 0,
        lines: ["Congrats, Hannah! Nathan? I think I saw him heading toward the chapel."],
      },
      {
        name: "Lexi",
        required: true,
        hint: "Lexi outside the chapel",
        sprite: "grads",
        frame: 1,
        lines: ["Nathan? You JUST missed him!", "He said something about the ceremony chairs?"],
      },
      {
        name: "Micheal",
        required: true,
        hint: "Micheal down by the lake",
        sprite: "grads",
        frame: 2,
        lines: ["Yo Hannah Congrats!", "Where's Nathan?", "He's probably working on some important AI club business right now I'm not sure where hes at."],
      },
      // Families in the ceremony chairs ("a"), in map order (frames in tools/seated_sprite.py).
      { at: "a", sprite: "seated", frame: 0, lines: [] },
      { at: "a", sprite: "seated", frame: 1, lines: [] },
      { at: "a", sprite: "seated", frame: 2, lines: [] },
      { at: "a", sprite: "seated", frame: 3, lines: [] },
      { at: "a", sprite: "seated", frame: 4, lines: [] },
      { at: "a", sprite: "seated", frame: 5, lines: [] },
      { at: "a", sprite: "seated", frame: 15, lines: [] },
    ],
    goal: {
      tile: "G",
      locked: ["A graduation cap left on a chair... Look around first."],
      // Once the notes are found, but not everyone's been talked to. {who} is whoever's left.
      lockedTalk: ["A graduation cap left on a chair...", "Maybe one of your classmates saw where he went. Try {who}."],
      lines: [
        "A graduation cap, left on a chair. The tassel's already turned.",
        "There's a note tucked inside:",
        "\"Congrats, Hannah! I'm so proud of you <3 Keep looking I'm still not here -Nathan\"",
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
    music: "moving",
    intro: ["Moving day. Goodbye, Rogers Park thank god!", "Carry every box to the U-Haul."],
    // Off down the alley with one box, leaving her the rest.
    glimpse: {
      path: [[18, 6], [18, 7], [39, 7]],
      carry: "box",
      lines: ["Was that Nathan, carrying only ONE box?","Bum", "...Guess the rest are up to me."],
    },
    // A neighbor out for a walk down the alley.
    people: [
      { look: 25, path: [[1, 7], [38, 7]], lines: ["Moving out? Good luck with all that.", "I'd help, but I just got back from the gym."] },
    ],
    details: {
      k: ["A stray cat. It watches you carry boxes.", "Kind of like that one we saw almost two years ago off the pier.", "It does not offer to help.", "Hater ass cat."],
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
    notes: [{ title: "Moving day", caption: "Goodbye Rogers Park, Hello Lakeview! Also what TF was Ethans shirt", photo: "public/photos/chapter_4/the_move.jpeg" }],
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
    // Golden morning light.
    tint: [255, 170, 60, 0.17],
    wall: "brick",
    floors: { ":": "sidewalk", ";": "road", "-": "roadLine", "=": "crosswalk" },
    // Characters for this chapter only: the pop-up's sign (three wide) over its
    // window (glass, the open window, glass), the pickup table with the bag,
    // the chalkboard, a bike rack, taxis both ways.
    objects: {
      S: "deckerSign", "(": "popupWindowL", w: "popupWindowM", ")": "popupWindowR",
      X: "pickupTable", m: "bagelMenu", k: "bikeRack", F: "fireEscapeFront", A: "taxi", a: "taxiEast",
    },
    music: "morning",
    intro: ["The last date before your new job.", "First stop: Decker's Bagels."],
    // Leaving the pickup table, grinning.
    glimpse: {
      path: [[10, 5], [13, 5], [13, 6], [15, 6]],
      lines: ["Hold on... was that Nathan, grinning about something?", "Gone again."],
    },
    // The line at the window, facing it. They turn around to talk.
    people: [
      { look: 14, at: [6, 4], face: "up" },
      { look: 12, at: [6, 5], face: "up", lines: ["Worth the wait. Trust me."] },
      {
        look: 13,
        at: [6, 6],
        face: "up",
        lines: ["Somebody just ordered two sandwiches and took off grinning.", "Said something about dinner plans?"],
      },
      // A jogger on the sidewalk.
      { look: 26, path: [[2, 8], [13, 8]], speed: 48 },
    ],
    map: [
      "##II###II###II##",
      "##II###II###II##",
      "######SSS#######",
      "##I###(w)###I###",
      ":m:::::::X:::k::",
      "::Y:::::::::::Y:",
      "::::::::::1:::::",
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
    // The worker leaning out of the window (`at` puts her in the window tile
    // instead of on an N).
    npcs: [
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
    floors: { ".": "woodDark", ",": "slate", a: "woodDark", b: "woodDark", y: "woodDark", z: "woodDark" },
    // Characters for this chapter only: sake shelves and lit box signs on the
    // slat walls, noren curtains in the doorways, the chefs' back counter (c),
    // the U-shaped hinoki counter ([ and ] are its arms, = its front, { and }
    // the corners, G your saved spot, E his: an empty plate), stools, standing
    // lit signs, lanterns, and the chefs' steel prep table (I, two by two).
    // Diners: "u" is a stool someone's sitting on, facing the counter; "a" and
    // "b" are diners on the arms' stools facing right and left, "y" and "z"
    // at a table (the people come from `npcs`). "j" is his jacket on his stool.
    objects: {
      K: "sakeShelf", L: "boxSign", n: "noren", c: "prepCounter",
      "[": "hinokiL", "]": "hinokiR", "=": "hinokiFront", "{": "hinokiBL", "}": "hinokiBR", G: "hinokiSando",
      E: "hinokiEmpty", o: "stool", u: "stool", j: "stoolJacket", A: "andon", l: "lantern", I: "prepIsland",
    },
    music: "yokocho",
    intro: ["Dinner at Yokocho, in the West Loop.", "Handrolls at the counter... and hopefully Nathan."],
    map: [
      "#KK#L##n##L#KK##",
      "#...[cccccc]...#",
      "#.l.[,,,,,,].l.#",
      "#..a[N,,,,,]b..#",
      "#...[,,II,,]...#",
      "#..a[,,II,N]b..#",
      "#...[,,,,,,]...#",
      "#..a[,,,,,,]b..#",
      "#.l.{==GE==}.l.#",
      "#....u.oj.u....#",
      "#..............#",
      "#A.yTz....hTh.A#",
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
      // Diners, in map order (frames in tools/seated_sprite.py): on the left
      // arm facing right, the right arm facing left, then the front.
      { at: "a", sprite: "seated", frame: 9, lines: [] },
      { at: "a", sprite: "seated", frame: 10, lines: [] },
      { at: "a", sprite: "seated", frame: 11, lines: [] },
      { at: "b", sprite: "seated", frame: 16, lines: ["Try the scallop one. Trust me."] },
      { at: "b", sprite: "seated", frame: 17, lines: [] },
      { at: "b", sprite: "seated", frame: 18, lines: [] },
      {
        at: "u",
        sprite: "seated",
        frame: 6,
        lines: ["Are those two seats yours?", "Someone left a jacket on one to hold them. Very serious about it."],
      },
      { at: "u", sprite: "seated", frame: 7, lines: [] },
      // A couple at a table (tools/local_sprite.py).
      { at: "y", sprite: "locals", frame: 36, lines: [] },
      { at: "z", sprite: "locals", frame: 52, lines: [] },
    ],
    details: {
      j: ["His jacket, on the stool next to yours.", "He can't have gone far."],
    },
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
    // patio heaters, and the DJ's booth (Q, two wide) between two speakers,
    // by the railing to the left of your table.
    // People sit at the tables: "a" is a seat on the left of a table, "b" on
    // the right, "m" is behind the bar, "d" behind the decks (they're all
    // deck underneath; the people come from `npcs`).
    floors: { ".": "deck", a: "deck", b: "deck", m: "deck", d: "deck" },
    objects: { V: "view", k: "cityLights", c: "bar", T: "bistroTable", H: "heater", Q: "djBooth", Z: "speaker" },
    music: "rooftop",
    intro: ["The rooftop of the Carbide & Carbon Building.", "Drinks after dinner, to celebrate your new job."],
    // Right after the intro, the camera finds him at the railing. He turns
    // around, and she says `lines`.
    reveal: { lines: ["...Nathan?", "He's really here."] },
    map: [
      "VVVVVVVVVVVVVV",
      "VVVVVVVVVVVVVV",
      "VVVVVVVVVVVVVV",
      "VVVVVVVVVVVVVV",
      "krrrrrrrrrrrrk",
      "krp.d..hXN.prk",
      "krZQQZ......rk",
      "kroooooooooork",
      "kr.aTb..aTb.rk",
      "kr....H.....rk",
      "kr.aTb...Tb.rk",
      "kroooooooooork",
      "kr..........rk",
      "kr....H..m..rk",
      "krp.....cccprk",
      "kr....P.....rk",
      "######EE######",
      "##############",
    ],
    // No notes here: she has to talk to the DJ and the bartender before him.
    notes: [],
    npcs: [
      // Looking out at the view (frame 3: facing up).
      { name: "Nathan", sprite: "nathan", frame: 3, lines: [] },
      // Guests at the tables, in map order: seats "a" face right, "b" face
      // left (frames in tools/local_sprite.py; everyone's a different person).
      // Guests with no lines just enjoy the view.
      { at: "a", sprite: "locals", frame: 7, lines: ["Cheers! We're celebrating too."] },
      { at: "a", sprite: "locals", frame: 8, lines: [] },
      { at: "a", sprite: "locals", frame: 10, lines: ["You can see the whole river from up here."] },
      { at: "b", sprite: "locals", frame: 13, lines: [] },
      { at: "b", sprite: "locals", frame: 38, lines: ["That guy by the railing keeps checking the elevator.", "Friend of yours?"] },
      { at: "b", sprite: "locals", frame: 39, lines: [] },
      { at: "b", sprite: "locals", frame: 40, lines: ["Best seat in the city."] },
      {
        name: "DJ",
        required: true,
        hint: "the DJ",
        at: "d",
        sprite: "locals",
        frame: 16,
        reach: 34,
        lines: ["Any requests?", "...The guy by the railing already asked for a slow one.", "Said he's waiting for someone."],
      },
      {
        name: "Bartender",
        required: true,
        hint: "the bartender",
        at: "m",
        sprite: "locals",
        frame: 15,
        reach: 34,
        lines: ["What can I get you?", "Oh, you're Hannah. Your drink's already waiting at his table."],
      },
    ],
    // The goal here is Nathan himself. With `view`, she walks up beside him,
    // they face each other for the `lines`, then both turn to look out at the
    // skyline for the `end`.
    goal: {
      tile: "N",
      view: true,
      speaker: "Nathan",
      locked: ["Not yet!"],
      // Until she's talked to the DJ and the bartender. {who} is whoever's left.
      lockedTalk: ["Not yet! Go say hi to {who} first."],
      lines: [
        "You found me.",
        "Sorry for making you chase me through our whole year.",
        "Every note was leading you here.",
      ],
      cards: [],
      end: [
        "Happy anniversary, Hannah.",
        "But I have one more gift for you.",
        "This one isn't a memory yet. It's for the future.",
        "Come on. I'll show you.",
      ],
      endSpeaker: "Nathan",
      advance: true,
      // Fade to black on the way to the jazz club.
      fade: true,
    },
  },
  {
    // The last gift: a night out that hasn't happened yet.
    chapter: "Someday soon",
    name: "Andy's Jazz Club",
    background: "#1a1420",
    // The house lights down low...
    tint: [22, 8, 12, 0.58],
    // ...and a spotlight on the singer ([column, row]).
    spotlights: [[9, 2]],
    wall: "brick",
    // Nathan walks in with her this time, a step behind.
    companion: { sprite: "nathan" },
    // "," is the stage, "_" the floor behind the bar. The band and the
    // bartender stand in their own tiles: "i" the pianist's bench, "v" the
    // singer and the sax player, "q" the drum kit, "m" behind the bar.
    floors: { ".": "clubCarpet", ",": "stage", _: "woodDark", a: "clubCarpet", b: "clubCarpet", m: "woodDark", i: "stage", v: "stage" },
    // Characters for this chapter only: the back bar (K) and the bar (c) with
    // stools, the curtain behind the stage, the neon sign (A, two wide), jazz
    // photos and wall lamps, the piano (two wide) and drums, candlelit
    // tables, your reserved table (Y), the host stand, plants and the door.
    objects: {
      K: "backBar", c: "clubBar", o: "stool", C: "curtain", A: "andysSign", F: "jazzPhoto", J: "sconce",
      p: "piano", q: "drums", T: "jazzTable", Y: "reservedTable", h: "hostStand", g: "plant", E: "door",
    },
    // The band's playing.
    music: "andys",
    intro: ["Andy's Jazz Club, downtown.", "The band's already playing."],
    map: [
      "#KKKKFCCAACCJFJ#",
      "#_m__.,pp,q,...#",
      "#cccc.,i,v,v...#",
      "#oooo.,,,,,,...#",
      "#.......Y......#",
      "#.aTb.......aTb#",
      "#g.............#",
      "#.aTb..aTb.....#",
      "#...........N.g#",
      "#.aTb.......h..#",
      "#..............#",
      "#..........P..g#",
      "###########E####",
    ],
    notes: [],
    npcs: [
      {
        name: "Host",
        sprite: "locals",
        frame: 21,
        reach: 34,
        lines: ["Welcome to Andy's!", "Reservation for two? Right this way.", "Your table's up front, right by the stage."],
      },
      // The band. They're busy playing, except the singer.
      { at: "i", sprite: "locals", frame: 17, sway: true, lines: [] },
      { at: "q", sprite: "locals", frame: 18, sway: true, lines: [] },
      { name: "Singer", at: "v", sprite: "locals", frame: 19, sway: true, reach: 30, lines: ["Welcome in, you two.", "This next one's a slow one."] },
      { at: "v", sprite: "locals", frame: 20, sway: true, lines: [] },
      { name: "Bartender", at: "m", sprite: "locals", frame: 22, reach: 34, lines: ["What can I get you two?", "Grab your table first. The set's already started."] },
      // Guests at the tables, in map order: seats "a" face right, "b" face
      // left (different people from the rooftop's).
      { at: "a", sprite: "locals", frame: 26, lines: ["First time at Andy's? You're in for a treat."] },
      { at: "a", sprite: "locals", frame: 27, lines: [] },
      { at: "a", sprite: "locals", frame: 28, lines: [] },
      { at: "a", sprite: "locals", frame: 29, lines: ["I come here every chance I get."] },
      { at: "a", sprite: "locals", frame: 30, lines: [] },
      { at: "b", sprite: "locals", frame: 46, lines: ["Shh... the sax solo's coming up."] },
      { at: "b", sprite: "locals", frame: 47, lines: [] },
      { at: "b", sprite: "locals", frame: 48, lines: ["You two look like you're celebrating."] },
      { at: "b", sprite: "locals", frame: 49, lines: [] },
      { at: "b", sprite: "locals", frame: 50, lines: [] },
    ],
    // The goal is the reserved table: they sit down across from each other,
    // and he gives her the tickets.
    goal: {
      tile: "Y",
      meet: true,
      speaker: "Nathan",
      locked: [],
      lines: ["Front row, right by the band.", "So... about that one more gift."],
      ticket: {
        label: "ONE MORE GIFT",
        admit: "ADMIT TWO",
        venue: "Andy's Jazz Club",
        detail: "Live jazz · River North",
        // TODO: the real date and time of the show.
        date: "Friday October 23rd · 7:45 PM",
        stub: "Seat: next to me 😼",
        caption: "",
      },
      end: ["I can't wait.", "Here's to year three, Hannah."],
      endSpeaker: "Nathan",
      advance: true,
      fade: true,
    },
  },
];

export const ENDING = {
  music: "title",
  signoff: "Happy anniversary, Hannah. ♥",
  closing: "Love, Nathan",
};
