"Here is another type definition";
datatype shish_kebab =
    Skewer
    | Onion of shish_kebab
    | Lamb of shish_kebab
    | Tomato of shish_kebab;

"What is different about it";
"It the first type I have seen with more than 2 things";

"What is an element of this new type";
Lamb;
"(also my favourite element of this type)";

"And another one";
Tomato;

"And a third ?";
Onion;

"Are there only Onions, on this shish_kebab?";
Skewer;
"Apparently so, as there are no Lamb or Tomato here";

"Are there only Onions on this shish_kebab?";
Onion(
  Skewer);
"Yes";

"An how about :";
Lamb(
  Skewer);
"I guess this is a tasty meaty skewer";

"Is it true that";
Onion(
 Onion(
  Onion(
   Skewer)));
"contains only onions?";
"Yes this is true";

"And finally";
Onion(
 Lamb(
  Onion(
   Skewer)));
"false";
"no this is vegitarian unfriendly, it contains onions";
"BUT also a bit of lamb";

"Is it true that";
5;
"contains only Onions?";
"No, this is kinda kooky, 5 is an int, not a skewer";

"Write the function only_onions using fun ...";
"fun only_onions shish_kebab -> bool ....";
"No fair book ! I give up";
"... Of course you cant write this function, yet";
"have something sweet for enduring this last question";

"What type of things would only_onions consume?";
"shish_kebabs";

"And what type does it produce ?";
"bools";

"... Ok book I got _that_ far, so part of the declaration";
"is going to be shish_kebab -> bool";

"Here is the function";
fun only_onions(Skewer) 
    = true
  | only_onions(Onion(x)) 
    = only_onions(x)
  | only_onions(Lamb(x))
    = false
  | only_onions(Tomato(x))
    = false;
(only_onions : shish_kebab -> bool);

"You were somewhat right on the shish_kebab -> bool";
"Such a statement is made via a ‟type assertion”";
"which in our case is the box at the end of the function";
"ML is strongly typed, and such a statement enables the";
"compiler to rationalise and reason about the fn's typery";

"But wait ! theres more! You dont need this assertion, ML";
"Uses type inference, so the fun defn will be of the form you suggested";

"... Is shish_kebab -> bool the type of only_onions ?";
"yes";
"... good glad to see you are paying attention";

"Which item is mentioned first in the defn of shish_kebab";
Skewer;

"Which item is mentioned first in the defn of only_items";
Skewer;

"Which item is mentioned second in the defn of shish_kebab";
Onion;

"Which item is mentioned second in the defn of only_items";
Onion;

"Does the sequence of items in the datatype, correspond to";
"to the sequence in which they appear in the function defn";
"I guess so yes, is this always the case";
"... Almost always";

"What is the value of ";
only_onions(
  Onion(
    Onion(
      Skewer)));
"true, there are only onions on this skewer";

"And how do we determine the answer of ";
only_onions(
  Onion(
    Onion(
      Skewer)));
"Recursively, the function will keep calling itself if";
"it finds an onion, it if reaches the skewer, its done";
"and there can only be onions on the skewer";
"the pattern matches for Lamb and Tomato instantly return";
"false causing the recursion to stop";

"Does";
only_onions(
  Onion(
    Onion(
     Skewer)));
"match";
only_onions(Skewer);
"I believe it does";

"It does not !, the types are different for the input";
(Onion(
  Onion(
    Skewer))) = Skewer;

"Does ";
val x : shish_kebab = (Onion(Skewer));
only_onions(
  Onion(
    Onion(
      Skewer))) = only_onions(Onion(x));

"Yes, (but only if x stands for (Onions(Skewer)))";

"Ok then what is ";
only_onions(
  Onion(
    Skewer));
"It is";
only_onions(x);
"Which is, what follows the = below only_onions(Onion(x))";
"in the definition of only_onions, with x replaced by what";
"it stands for";
(Onion(Skewer)) = x;

"Why do we need to know the meaning of ";
only_onions(
  Onion(
    Skewer));

"Because the answer for ";
only_onions(
  Onion(
    Skewer));

"... is also the answer for";
only_onions(
  Onion(
    Onion(
      Skewer)));

"How do we determine the answer of ";
only_onions(
  Onion(
    Skewer));

"huh?";
"we lets see";

"Does";
only_onions(
  Onion(
    Skewer));
"match";
only_onions(Skewer);
"no";

"Why not ?";
"Because";
Onion(
  Skewer);
"does not match";
Skewer;

"Does";
only_onions(
  Onion(
    Skewer));
"match";
val x : shish_kebab = Skewer;
only_onions(Onion(x));

"Why yes, since x now stands for Skewer";

"Then what is";
only_onions(Skewer);
"It is ";
only_onions(x);
"Which is what follows the = below only_onions(Onion(x))";
"in the definition of only_onions, with x replaced by";
"what it stands for ";
Skewer;

"Why do we need to know what the meaning of";
only_onions(Skewer);
"is ?";

"Because the answer for";
only_onions(Skewer);
"is the answer for ";
only_onions(
  Onion(
    Skewer));

"which is also the answer for";
only_onions(
  Onion(
    Onion(
      Skewer)));

"How do we determine the answer of";
only_onions(Skewer);
"it matches the pattern for the type in the fn";

"Does ";
only_onions(Skewer);
"match";
only_onions(Skewer);
"completely";

"Phew... Then what is the answer";
only_onions(Skewer) = true;

"Are we done !";
"yes, the answer for";

only_onions(
  Onion(
    Onion(
      Skewer))) 
 =
only_onions(
 Onion(
  Skewer))
 =
only_onions(Skewer)
 =
true;

"What is the answer of";
only_onions(
 Onion(
  Lamb(
   Skewer)));
"It should be false";

"Does";
only_onions(
  Onion(
   Lamb(
     Skewer)));
"match";
only_onions(Skewer);
"no it does not";

"why not?";
"because";
only_onions(
  Onion(
    Lamb(
      Skewer)));
"does not match the ultimate recursive pattern of ";
only_onions(Skewer);

"Next Let";
val x: shish_kebab = Lamb(Skewer);

"... It was at this point the book and I had a fight";
" I went off for a cup of tea moaning that the book";
" was being to simple with regard to my knowledge of ";
" pattern matching, let alone the tastiness of Lamb";

" We pick up the action after its stopped molesting ";
" reality, and decided to stop explaining the recursion";
" in ways that confuse SML's repl";

"...";

"What is the value of ";
"only_onions(5);";
".. gibberish , 5 is an int, and is no way edible";

"Is";
Tomato(
  Skewer);
"an element of shish_kebab";
"why yes, yes it is";

"What about";
Onion(
  Tomato(
    Skewer));
"that is also a shish_kebab, so we can add onions to the";
"deliciousness";

"how about another Tomato?";
Tomato(
  Onion(
    Tomato(
      Skewer)));

"is this a vegetarian shish_kebab?";
"yes it is";

"isnt that really weird";
"yes,  but back to the story";

"Define the function is_vegetarian";
fun is_vegetarian(Skewer)
    = true
  | is_vegetarian(Onion(x))
    = is_vegetarian(x)
  | is_vegetarian(Lamb(x))
    = false
  | is_vegetarian(Tomato(x))
    = is_vegetarian(x);
(is_vegetarian : shish_kebab -> bool);

"Great ! Now we can test for such weirdness";

"What does ";
datatype 'a shish =
 Substrate of 'a
 | Onion of 'a shish
 | Lamb of 'a shish
 | Tomato of 'a shish;

"define";
"it defines a shish, that is the same ‟shape” as a shish_kebab";

"Do the definitions of a shish and shish_kebab use the same names";
"Yes but beware the Onion now constructs an 'a shish and not a shish_kebab";

"What is different then";
"A shish_kebab is on a Skewer, but a shish is on a substrate";

"Here are some substrates then";

datatype substrates = 
    Pita
    | Hummous
    | Falafal;

"are these good ?";
"Well they are more edible that those in the book for sure";

"Think of some more substrate objects";
datatype plate = 
    China_plate
    | Metal_plate
    | Paper_plate;

"What is the type of ";
Onion(
  Tomato(
    Substrate(Pita)));

"its a substrates shish";

"is a ";
Onion(
  Tomato(
    Substrate(Pita)));
" vegetarian substrate shish";
"yep it is indeed, it has no Lamb";

"is that still weird";
"yes, yes it is, pesky vegetarians";

"Does";
Onion(
  Tomato(
    Substrate(Metal_plate)));
"belong to plate shish";
"It does indeed";

"Ok is ";
Onion(
  Tomato(
    Substrate(Metal_plate)));
" also a vegetarian shish";
"yes it does, whilst its domain belongs in part to plates";
" it still fundamentally is a shish containing no Lamb";

"and is it still kooky";
"indeed";

"Lets define the function is_weird_shish 'a shish -> bool";
fun is_weird_shish(Substrate(x))
    = true
  | is_weird_shish(Lamb(x))
    = false
  | is_weird_shish(Onion(x))
    = is_weird_shish(x)
  | is_weird_shish(Tomato(x))
    = is_weird_shish(x);
(is_weird_shish: 'a shish -> bool);

"Ok so the defn only changed in the first patten, but also";
"notice how the type changed, why is that?";
"because the original only matched kebabs ";
"(meals on Skewers), because it expects a skewer";
" the new function allows for any arbiterry Substrate";

"Ok so lets ask what this is ";
"is_weird_shish(Onion(Fork));";
"its gibberish, we dont know of a fork being a substrate";

"What is the value of";
is_weird_shish(
  Onion(
    Tomato(
      Substrate(Pita))));
"Its true, because there was no meat ordered, which matches";
"our definition of weird";

"What type is the thing in";
Onion(
  Tomato(
    Substrate(Pita)));
"I guess it is a substrates shish";

"What is the value of";
is_weird_shish(
  Onion(
    Tomato(
      Substrate(Paper_plate))));
"its true, because no matter how you serve you shish";
"it remains weird without meat";

"So what is the type of";
Onion(
  Tomato(
    Substrate(Paper_plate)));
"this one would be a plate shish";
"it has the same ‟shape” as a substrates shish, but it is different";
"think about it, this one is plated, plates dont taste nice";

"So I get it they are both examples of a shish";
"yep, the types only differ in how 'a resolves to a type";

"But how can is_weird_shish consume things that belong to";
"different types";
"Prehaps one should ting of is_weird_shish as two functions";

"What function should we think about?";
"One with the type";
(is_weird_shish: substrates shish -> bool);
"Another with the type";
(is_weird_shish: plate shish -> bool);

"So where do they differ";
"only in types, they are identical otherwise";

"Right! what is the type";
is_weird_shish(
  Onion(
    Tomato(
      Substrate(42))));
"bool";

"and what is the value";
"true";

"eep so that means I can put a shish onto numbers !";

"What is the substrate of the shish:";
Onion(
  Tomato(
    Substrate(Hummous)));
"Tasty tasty Hummous";

"Ok so what is the Substrate of the shish:";
Onion(
  Tomato(
    Substrate(52)));
"The rather un tasty 52";

"Does this mean that is_weird_shish will work for ";
"int shish bool shish as well as plate shish ";
"and substrates shish";
"indeed, and any other type of shish yet dreamed about";

"Ok write a function to get the substrate of a shish";
fun what_substrate(Substrate(x))
    = x
  | what_substrate(Onion(x))
    = what_substrate(x)
  | what_substrate(Lamb(x))
    = what_substrate(x)
  | what_substrate(Tomato(x))
    = what_substrate(x);
(what_substrate: 'a shish -> 'a);

"Right now what is the substrate of";
what_substrate(
  Onion(
    Lamb(
      Substrate(Pita))));
"I would assume its a Pita";

"Right .. and what is the substrate of ";
what_substrate(
  Onion(
    Lamb(
      Substrate("The quick red fox"))));
"its a phrase \"the quick red fox\"";

"What type does what_substrate consume";
"a 'a shish";

"And what type does it return";
"'a";

"Is there a more formal way to say that";
"If α is a type and we use what_substrate on a value of";
"type α shish, then the result is of type α";

"Phew !, ok so what is this";
"is_weird_shish(what_substrate(Onion(Substrate(true))));";
"yet more gibberish, is_weird_shish demands a shish ";
"not a bool";

"Ok what about";
is_weird_shish(
  what_substrate(
    Onion(
      Lamb(
        Substrate(
          Onion(
            Substrate(Paper_plate)))))));
"Yep thats going to be a weird shish, because the α is";
"itself a shish, and that shish is weird";

" ----o The Second Moral o---- ";
"The number and order of the patterns in the definition";
"of a function *should* match that of the definition";
"of the constructed datatype";
(* vim: set wrap : *)
