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
    floors: { ".": "wood", ",": "kitchen", ":": "rug", "'": "woodPetals" },
    // Characters for this chapter only: the chalkboard menu by the door.
    objects: { m: "menuBoard" },
    intro: ["February 14th. 1055 W Pratt, apartment 2A.", "Something smells amazing... but where's Nathan?"],
    map: [
      "##ww##ww###ww#w####www####w###ww#w##",
      "#p......p#.BBj.p#p..jBB.#t.u#p.jBB.#",
      "#........#.bb...#....bb.#...#...bb.#",
      "w..hXh...#......#.......#...#......#",
      "w...''...#....1.#.......#...#...3..#",
      "#....''..#......#.......#...#......#",
      "#...v.'..#......#....L..#...#......#",
      "#......'.####.####.######.###,######",
      "#..(C).'..................,,,,,cOkf#",
      "#.(:::..'.............2...,,,,,,,,c#",
      "#.C:::.m.'P#########.###.##,,,,,,,c#",
      "w.):::...#D#     #t....#..#,,,,,,,,#",
      "w...v....#       #.....#..#,,,,,,,,#",
      "##########       ###########D###ww##",
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
    name: "New York City",
    background: "#1a1420",
    wall: "brick",
    door: "subway",
    floors: { ".": "grass", ",": "path", ":": "sidewalk", ";": "road", "-": "roadLine", "=": "crosswalk", _: "terracotta" },
    // Characters for this chapter only.
    objects: {
      q: "waterBoat", y: "waterDucks", A: "taxi", a: "taxiEast", z: "hotDogCart",
      // Chinatown: fire escapes, the shops, the dumpling house, fruit stands and lanterns.
      F: "fireEscapeFront",
      R: "shopRed", J: "shopJade", M: "shopMarket", K: "shopDucks", B: "shopBakery",
      V: "restaurant", g: "fruitStand", i: "lanterns",
    },
    intro: ["New York City.", "Nathan has to be around here somewhere."],
    map: [
      "HHHHHHHHHHHHHHHHHHHH",
      "H........,,........H",
      "H.Y......P,....Y...H",
      "H....Y...,,e.......H",
      "H........,,........H",
      "H........,,..~~~...H",
      "H......n..,,~y~~~..H",
      "H..Y......,,~~~~~..H",
      "H........e,,~~q~~..H",
      "H.........,,~~~~~..H",
      "H.....Y...,,.~~~...H",
      "H.........,,.......H",
      "H.........,,nn1....H",
      "H.Y......,,........H",
      "H.......,,e.....Y..H",
      "H......Y,,.........H",
      "H.......,,.........H",
      "H.......,,...Y.....H",
      "H...Y...,,.........H",
      "H.......e,,......Y.H",
      "H.Y......,,........H",
      "H........,,........H",
      "HHHHHHHH,,,,HHHHHHHH",
      ":::::::::::::z::::::",
      "--AA----====--------",
      ";;;;;;;;====;;;aa;;;",
      "::::::::::::::::::::",
      "#IIFFIII::::IIIFFII#",
      "#IIFFIII::::IIIFFII#",
      "#BRKJMRJ::::MRJKBRJ#",
      "#::::g::::::g::::::#",
      "#iiiiiiiiiiiiiiiiii#",
      "#::::::::::::::::::#",
      "#IIFFIII:::IIFFIIII#",
      "#IIFFIII:::IIFFIIII#",
      "#KRJBMRJ:::RVVVVVVJ#",
      "#::::g::::::______:#",
      "#iiiiiiiiiiiiiiiiii#",
      "#:::::::::::_hZh__:#",
      "#:::::::::::______:#",
      "#:::2:::::::______:#",
      "#:::::::::::p::::p:#",
      "#::::::::::::::::::#",
      "#::::::::::::::::::#",
      "#::::::::D:::::::::#",
      "####################",
    ],
    notes: [
      { title: "Central Park", caption: "The part of the trip that stood out most. We could have walked around here all day.", photo: null },
      { title: "Chinatown", caption: "We kept finding our way back here.", photo: null },
    ],
    npcs: [],
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
    floors: { ".": "road", ",": "sidewalk" },
    // Characters for this chapter only: parked cars (two tiles tall), the
    // building's front door (two wide) and traffic cones.
    objects: { A: "car", a: "frontDoor", i: "cone" },
    intro: ["Moving day. Goodbye, Rogers Park.", "Carry every box to the U-Haul."],
    map: [
      "####I#I##I#I####",
      "####I##aa##I####",
      "###,,,,,,,,,,###",
      "###,...P....,###",
      "###,........Y###",
      "###,A....x..,###",
      "##F,A.......,###",
      "##F,.......A,###",
      "###,.......A,###",
      "###,QQ......,###",
      "###e........,F##",
      "###,........,F##",
      "###Y........,###",
      "###,x.......,###",
      "###,........,###",
      "###,......x.,###",
      "##F,........,###",
      "##F,.1.....A,###",
      "###,.......A,###",
      "###,A.......,###",
      "###,A.......Y###",
      "###,..x.....,###",
      "###,........,F##",
      "###,........,F##",
      "###,........e###",
      "###,.......x,###",
      "###,........,###",
      "###Y........,###",
      "###,...UU...,###",
      "###,...UU...,###",
      "###,A..UU...,###",
      "###,A.i..i..,###",
      "###,........,###",
      "################",
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
    chapter: "Chapter 5",
    name: "Chateau Carbide",
    background: "#1b2340",
    // Tints the world dark blue and makes the string lights and candle glow.
    night: true,
    wall: "decoWall",
    floors: { ".": "deck" },
    // Characters for this chapter only: the night sky and moon above the
    // skyline, city lights far below the railings, the bar, candlelit cafe
    // tables and patio heaters.
    objects: { S: "nightSky", M: "moon", k: "cityLights", c: "bar", T: "bistroTable", H: "heater" },
    intro: ["The rooftop of the Carbide & Carbon Building.", "Dinner to celebrate your new job."],
    map: [
      "SSSSSSSSSSSSSSSMSSSS",
      "KKKKKKKKKKKKKKKKKKKK",
      "krrrrrrrrrrrrrrrrrrk",
      "krp..............prk",
      "kr......hXN.......rk",
      "kr................rk",
      "kr...............prk",
      "kroooooooooooooooork",
      "kr................rk",
      "kr.........H...2..rk",
      "kr.hTh............rk",
      "kr................rk",
      "kr..1.............rk",
      "kr.H..............rk",
      "kroooooooooooooooork",
      "kr................rk",
      "krp...............rk",
      "kr..........hTh...rk",
      "kr.hTh............rk",
      "kr................rk",
      "kr.............H..rk",
      "krp..........ccccprk",
      "kr.......P........rk",
      "#########EE#########",
      "####################",
      "####################",
    ],
    notes: [
      { title: "Chateau Carbide", caption: "Green and gold, the whole city lit up around us.", photo: null },
      { title: "Your new job", caption: "We came up here to celebrate before your first day. I'm so proud of you.", photo: null },
    ],
    npcs: [{ name: "Nathan", sprite: "nathan", lines: [] }],
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
