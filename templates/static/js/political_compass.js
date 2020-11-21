var compass_canvas;
const WIDTH=500;
const HEIGHT=500;

var highlight_index=-1;
const BOUNDING_BOXES=[
  [WIDTH*0.03, HEIGHT*0.03, WIDTH*0.465, HEIGHT*0.465], //Auth Left
  [WIDTH*0.5, HEIGHT*0.03, WIDTH*0.47, HEIGHT*0.465], //Auth Right
  [WIDTH*0.03, HEIGHT*0.5, WIDTH*0.465, HEIGHT*0.47], //Lib Left
  [WIDTH*0.5, HEIGHT*0.5, WIDTH*0.47, HEIGHT*0.47] //Lib Right
];

const BOX_CENTER=[(WIDTH*0.465-WIDTH*0.035)*0.5, (HEIGHT*0.465-HEIGHT*0.035)*0.5];

const NAMES=['Auth Left', 'Auth Right', 'Lib Left', 'Lib Right'];
const NAMES_SERVER=['auth-left', 'auth-right', 'lib-left', 'lib-right'];

const COLOURS=[
  [214, 63, 58], //Auth Left
  [58, 133, 214], //Auth Right
  [194,221,181], //Lib Left
  [237,237,161] //Lib Right
];

function setup(){
  compass_canvas=createCanvas(WIDTH, HEIGHT);
  compass_canvas.parent('compass_div');
}

function draw(){
  highlight_index=-1;
  for(var i=0; i<4; i++){
    if(BOUNDING_BOXES[i][0]<mouseX && mouseX<BOUNDING_BOXES[i][0]+BOUNDING_BOXES[i][2] && BOUNDING_BOXES[i][1]<mouseY && mouseY<BOUNDING_BOXES[i][1]+BOUNDING_BOXES[i][3]){
      highlight_index=i;
    }
  }


  background(0);
  fill(255);
  rect(WIDTH*0.025, HEIGHT*0.025, WIDTH*0.95, HEIGHT*0.95);

  strokeWeight(0);

  var colour;
  var alpha;
  for(var i=0; i<4; i++){
    if(highlight_index==i){alpha=255;}
    else{alpha=150;} //127.5
    fill(COLOURS[i][0], COLOURS[i][1], COLOURS[i][2], alpha);
    rect(BOUNDING_BOXES[i][0], BOUNDING_BOXES[i][1], BOUNDING_BOXES[i][2], BOUNDING_BOXES[i][3]);
    textSize(32);
    textAlign(CENTER);
    fill(0);
    //text(NAMES[i], BOUNDING_BOXES[i][0]+(BOUNDING_BOXES[i][0]+BOUNDING_BOXES[i][2])*0.5, BOUNDING_BOXES[i][1]+(BOUNDING_BOXES[i][1]+BOUNDING_BOXES[i][3])*0.5);
    text(NAMES[i], BOUNDING_BOXES[i][0]+BOX_CENTER[0], BOUNDING_BOXES[i][1]+BOX_CENTER[1]);
  }
  //Axes
  strokeWeight(10);
  stroke(0);
  line(WIDTH*0.5, 0, WIDTH*0.5, HEIGHT);

  strokeWeight(10);
  stroke(0);
  line(0, HEIGHT*0.5, WIDTH, HEIGHT*0.5);
}

function mousePressed(){
  for(var i=0; i<4; i++){
    if(BOUNDING_BOXES[i][0]<mouseX && mouseX<BOUNDING_BOXES[i][0]+BOUNDING_BOXES[i][2] && BOUNDING_BOXES[i][1]<mouseY && mouseY<BOUNDING_BOXES[i][1]+BOUNDING_BOXES[i][3]){
      console.log(NAMES[i]);
      window.location.href='/articles\?category='+NAMES_SERVER[i];
    }
  }
}
