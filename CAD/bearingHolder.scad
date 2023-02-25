bearingSize=12; //diameter of ball bearing used
baseWidth=16;
baseLength=24;
baseThickness=3.75; 
screwSize=1.5;  //M2 screw self-threading
screwSpace=16.5; // distance center-center for screws
topWidth=bearingSize*1.5;
tolerance=.5; //.5 slides in well has minimal movement, used surrounding ball bearing

difference(){
    union(){
        //base
        translate([0,0,-baseThickness/2])
        cube([baseWidth, baseLength, baseThickness], center=true);
        //top section, holds bearing
        translate([0,0,2*bearingSize/6])
        cylinder(d=topWidth, h= 2*bearingSize/3, center=true, $fn=60);
}
//bearing
    translate([0,0,bearingSize/2])
    sphere(d=bearingSize+tolerance, $fn=60);
//notches for bearing movement
    translate([0,-topWidth/2,0])
    cylinder(h=2*bearingSize/3,d=topWidth/2, $fn=60);
    translate([0,topWidth/2,0])
    cylinder(h=2*bearingSize/3,d=topWidth/2, $fn=60);
    translate([topWidth/2,0,0])
    cylinder(h=2*bearingSize/3,d=topWidth/2, $fn=60);
    translate([-topWidth/2,0,0])
    cylinder(h=2*bearingSize/3,d=topWidth/2, $fn=60);
//screw holes
    translate([0,-screwSpace/2,0])
    cylinder(h=50, d=screwSize,center=true, $fn=60);
    translate([0,screwSpace/2,0])
    cylinder(h=50, d=screwSize,center=true, $fn=60);
}
