const functions = require('firebase-functions');
const express = require("express");
// const session = require('express-session');
const engines = require('consolidate');
const admin = require('firebase-admin');
const serviceAccount = require('./ServiceAccountKey.json');
const fs = require('fs');
const bodyParser = require('body-parser');
const exec = require('child_process').exec;
const path = require('path');
const firebase = require("firebase");


firebase.initializeApp({
    
});

admin.initializeApp({
    
});

const db = admin.firestore();

const app = express();
app.use(express.static('public'));
app.use(bodyParser.urlencoded({ extended: true }));
app.set('view engine', 'ejs');

app.get("/", (req, res)  => {
    res.set('Cache-Control', 'public, max-age=300,s-maxage=600');
    res.render("home");
    res.end();
});

// firebase.auth().onAuthStateChanged(function(user) {
//     if (user) {
//         // User is signed in.
//         console.log("*****************************signed in************************************");
//     } else {
//         console.log("*****************************signed out************************************");
//     }
// });


app.get("/home", function(req, res) {
  res.render("home");
  res.end();
});

app.get("/resource", function(req, res) {
  console.log("called");
  res.render("resources");
  res.end();
});


app.get("/signin", function(req, res) {
  res.render('signin', {message: null});
  res.end();
});

app.post("/signup", function(req, res) {

    const email = req.body.email;
    const password = req.body.password;
    const displayName = req.body.name;

    admin.auth().createUser({
        email: email,
        emailVerified: false,
        password: password,
        displayName: displayName,
        disabled: false
    }).then(function(userRecord) {
            // See the UserRecord reference doc for the contents of userRecord.
            console.log('Successfully created new user:', userRecord.uid);
            //login the person

        firebase.auth().signInWithEmailAndPassword(email, password).then(result => {

            firebase.auth().onAuthStateChanged(user => {
                if (user) {
                    res.json({worked: true, uid: firebase.auth().currentUser.uid, name: firebase.auth().currentUser.displayName});
                    res.end();
                } else {
                    // User is signed out.
                    res.json({worked: false, message: "no user"});
                    res.end();
                }
            });

        }).catch(function(error) {
            // Handle Errors here.
            var errorCode = error.code;
            var errorMessage = error.message;
            res.json({worked: false, message: errorMessage});
            res.end();
            // ...
        });


    }).catch(function(error) {
        var errorCode = error.code;
        var errorMessage = error.message;
        res.json({worked: false, message: errorMessage});
        res.end();
    });


});

app.post('/login', function(req,res) {

    // Build Firebase credential with the Google ID token.
    var email = req.body.email;
    var password = req.body.password;


    firebase.auth().signInWithEmailAndPassword(email, password).then(result => {
        firebase.auth().onAuthStateChanged(user => {
            if (user) {
                res.json({worked: true, uid: firebase.auth().currentUser.uid, name: firebase.auth().currentUser.displayName});
                res.end();
            } else {
                // User is signed out.
                res.json({worked: false, message: "no user"});
                res.end();
            }
        });

    }).catch(function(error) {
        // Handle Errors here.
        var errorCode = error.code;
        var errorMessage = error.message;
        res.json({worked: false, message: errorMessage});
        res.end();
        // ...
    });
});

app.get("/signing", function(req, res) { //redirects to signup
    res.render('signup', {message: null});
    res.end();
});

app.get("/portal", function(req, res) {
    res.render('portal');
   res.end();

});

app.post("/loaddata", function(req, res) {
// check if post exists
    var uid = req.body.uid;

    var docRef = db.collection("users").doc(uid);

    docRef.get().then(function(doc) {
        if (doc.exists) {
            console.log("we here");

            db.collection("users").doc(uid).get().then(doc => {
                console.log("got data in getprevious");
                console.log(doc.data());

                var answers = doc.data().previousA;
                var questions = doc.data().previousQ;
                var type = doc.data().type;
                var bounds = doc.data().bounds;

                var message = "";
                console.log("doing message");
                for(var i = answers.length-1; i >= 0; i--) {
                  if(type[i] == "limit") {
                    message += "the limit as x approaches " + bounds[i] + " of " + questions[i] + " is " + answers[i] + "<br>";
                  } else if (type[i] == "derivative" || type[i] == "integral"){
                    message += "the " + type[i] + " of " + questions[i] + " is " + answers[i] + "<br>";
                  } else if(type[i] == "definite integral") {
                    var lowerBound = bounds[i].substring(0, bounds[i].indexOf(","));
                    var upperBound = bounds[i].substring(bounds[i].indexOf(",")+1, bounds[i].length);
                    message += "the area under " + questions[i] + " from " + lowerBound + " to " + upperBound + " is " + answers[i] + "<br>";
                  } else if (type[i] == "summation") {
                    var lowerBound = bounds[i].substring(0, bounds[i].indexOf(","));
                    var upperBound = bounds[i].substring(bounds[i].indexOf(",")+1, bounds[i].length);
                    message += "the sum of " + questions[i] + " from " + lowerBound + " to " + upperBound + " is " + answers[i] + "<br>";
                  } else if (type[i] == "product") {
                    var lowerBound = bounds[i].substring(0, bounds[i].indexOf(","));
                    var upperBound = bounds[i].substring(bounds[i].indexOf(",")+1, bounds[i].length);
                    message += "the product of " + questions[i] + " from " + lowerBound + " to " + upperBound + " is " + answers[i] + "<br>";
                  }
                }
                console.log("message");
                console.log(message);

                res.json({error: false, previous: message});
                res.end();
            });

        } else {
            // doc.data() will be undefined in this case

            //create new document

            var data = { //previous questions, answers, and types
                previousQ: [],
                previousA: [],
                type: [],
                bounds: []
            };

            db.collection('users').doc(uid).set(data).then( ref => {
                res.json({error: false, previous: ""});
                res.end();
            });
        }
    }).catch(function(error) {
        console.log("Error getting document:", error);
        res.json({error: true, message: "Error getting document:" , error});
        res.end();
    });
});

app.post("/calc", function(req, res) { //for calculating calculus

    var equation = req.body.equation;
    var type = req.body.type;
    var bounds = req.body.bounds;
    var uid = req.body.uid;

    console.log("got data");
    //save to json

    var obj = {
        equation: equation,
        type: type,
        bounds: bounds
    };

    var json = JSON.stringify(obj);
    fs.writeFile('data.json', json, 'utf8', function() {
      console.log("done writing, now sending");
        //send to python
        var cmd = 'py -3.6 solve.py';
        exec(cmd, (err, stdout, stderr) => {
            if (err) {
                console.log(err);
                res.json({error: true, message: "there is an error, please try again"});
                res.end();
            }
            console.log("called python ye");

            var contents = fs.readFileSync("answer.json");
            // Define to JSON type
            var jsonContent = JSON.parse(contents);

            console.log(jsonContent.equation);

            //just add to previous now

            db.collection("users").doc(uid).get().then(doc => {
                console.log(doc.data());

                var answers = doc.data().previousA;
                var questions = doc.data().previousQ;
                var typeofq = doc.data().type;
                var allBounds = doc.data().bounds;

                //clean up equation before adding it

                //e, pi, exp

                equation = equation.replace(/pi/g, "π");
                equation = equation.replace(/E/g, "e");
                equation = equation.replace(/exp/g, "e^");

                var newAnswer = jsonContent.equation;

                newAnswer = newAnswer.replace(/pi/g, "π");
                newAnswer = newAnswer.replace(/E/g, "e");
                newAnswer = newAnswer.replace(/exp/g, "e^");


                //clean up exp

                //add to

                answers.push(newAnswer);
                questions.push(equation);
                typeofq.push(type);
                allBounds.push(bounds);


                //limit to 12
                if(answers.length > 12) {
                    answers.splice(0, answers.length - 12);
                    questions.splice(0, questions.length - 12);
                    typeofq.splice(0, typeofq.length - 12);
                    allBounds.splice(0, allBounds.length - 12)
                }

                //after reading, we write

                var data = { //previous questions, answers, and types
                    previousQ: questions,
                    previousA: answers,
                    type: typeofq,
                    bounds: allBounds
                };

                console.log("done pushing, now rendering");

                db.collection('users').doc(uid).set(data).then(ref => { //updated firestore
                    //now we render
                    console.log("done writing");
                    db.collection("users").doc(uid).get().then(doc => {

                        var answers = doc.data().previousA;
                        var questions = doc.data().previousQ;
                        var type = doc.data().type;
                        var bounds = doc.data().bounds;

                        var message = "";

                        for(var i = answers.length-1; i >= 0; i--) {
                          if(type[i] == "limit") {
                            message += "the limit as x approaches " + bounds[i] + " of " + questions[i] + " is " + answers[i] + "<br>";
                          } else if (type[i] == "derivative" || type[i] == "integral"){
                            message += "the " + type[i] + " of " + questions[i] + " is " + answers[i] + "<br>";
                          } else if(type[i] == "definite integral") {
                            var lowerBound = bounds[i].substring(0, bounds[i].indexOf(","));
                            var upperBound = bounds[i].substring(bounds[i].indexOf(",")+1, bounds[i].length);
                            message += "the area under " + questions[i] + " from " + lowerBound + " to " + upperBound + " is " + answers[i] + "<br>";
                          } else if (type[i] == "summation") {
                            var lowerBound = bounds[i].substring(0, bounds[i].indexOf(","));
                            var upperBound = bounds[i].substring(bounds[i].indexOf(",")+1, bounds[i].length);
                            message += "the sum of " + questions[i] + " from " + lowerBound + " to " + upperBound + " is " + answers[i] + "<br>";
                          } else if (type[i] == "product") {
                            var lowerBound = bounds[i].substring(0, bounds[i].indexOf(","));
                            var upperBound = bounds[i].substring(bounds[i].indexOf(",")+1, bounds[i].length);
                            message += "the product of " + questions[i] + " from " + lowerBound + " to " + upperBound + " is " + answers[i] + "<br>";
                          }
                        }
                        console.log("message");
                        console.log(message);
                        // session saved
                        console.log("saved");
                        res.json({error: false, answer: newAnswer, previous: message});
                        res.end();
                    });


                });

            });


        });
    });
});

app.post("/ml", function(req, res) {
    let data = JSON.parse(req.body);
    let image = data["img"];

    // Remove header
    let base64Image = image.split(';base64,').pop();

    fs.writeFile('math.png', base64Image, {encoding: 'base64'}, function(err) {
        console.log('File created');
        //now we do python
        var cmd = 'py -3.6 calculate2.py';
        exec(cmd, (err, stdout, stderr) => {
              if (err) {
                  console.log(err);
                  res.json({error: true, message: "you didn't draw something."});
                  res.end();
              }
              console.log("called python ye");

              var contents = fs.readFileSync("char.json");
              // Define to JSON type
              var jsonContent = JSON.parse(contents);
              console.log(jsonContent);
              var character = jsonContent["char"];

              res.json({error: false, character: character});
              res.end();
        });
    });

});


app.post("/clear", function(req, res) {
    var uid = req.body.uid;

    var data = { //previous questions, answers, and types
        previousQ: [],
        previousA: [],
        type: [],
        bounds: []
    };

    db.collection('users').doc(uid).set(data).then( ref => {
        res.json({});
        res.end();
    });
});

exports.app = functions.https.onRequest(app);
