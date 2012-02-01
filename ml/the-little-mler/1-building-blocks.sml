(*Control.Print.out := { say=fn _=>(), flush=fn()=>()};*)
"Is this a number -> 5?";
5; 
"yes";

"Is 5 also an integer ?";
5; 
"yes";

"Is this a number -> 17?";
17;
"yes and its also an int";

"Is this an integer -> 5.32 ?";
5.32; 
"No its a real";

"What type of number is 5 ?";
5; 
"Its an int";

"Quick ! think of another integer!";
12341;

"What type of value is true?";
"Its a bool";
true; 

"What tpye of value is false";
"also a bool";
false; 

"Can you think of another boolean ?";
"no";

"Are there more ints than booleans ?";
"Yes there are ∞ ints, but only 2 booleans";

"What is int ?";
"A type";

"What is bool ?";
"Another type";

"What is a type ?";
"A type is a name for a collection of objects";

"What is a type ?";
"Sometimes we it as if it were a collection";

"Does this define a new type ?";
datatype seasoning = Salt | Pepper;
"Yes it does";

"Is this seasoning";
Salt;
"Yes it is";

"And";
Pepper;
"Yes it is also a seasoning";

"Can you think of another seasoning";
"No only Salt and Pepper are seasonings (must make for bland food)";

"Have we seen a type like seasoning before?";
"Well boolean is like it I guess";

"Does this define a new type too?";
datatype num =
    Zero
    | One_more_than of num;
"Yes it does";

"Is this a num:";
Zero;
"Yes like Salt is a seasoning";

"Is this a num ?";
One_more_than(Zero);
"Yes it is, because One_more_than constructs a num from a num";

"How does One_more_than do that?";
"We give it Zero which is a num, and from that it constructs a new num";

"What is the type of";
One_more_than(
  One_more_than(
    Zero));
"I venture its a number good sir !";

"What is :";
"One_more_than(0);";
"nonsense I guess, 0 is not defined as _our_ type num";

"what is the type of";
One_more_than(
  One_more_than(
    One_more_than(
      One_more_than(
        Zero))));
"Its still a number";

"What is the difference between Zero and 0?";
"Zero is a num, 0 is an int";

"Correct In general, if two things belong to two different types";
"they cannot be the same";

"Are there more nums than bools?";
"Lots";

"Are there more nums than ints?";
"No they are both in essence ∞";

"What does this define?";
print "** NOTE: 'a is ascii for α\n";
datatype 'a open_faced_sandwich =
    Bread of 'a
    | Slice of 'a open_faced_sandwich;
"It is a new type, with a funny symbol";

"What is";
Bread(0);
"its an element of an open_faced_sandwich";

"Ok what about";
Bread(true);
"its also an element of an open_faced_sandwich";

"Huh? but they belong to two different types, Why is that!";

"Its because";
datatype 'a open_faced_sandwich =
    Bread of 'a
    | Slice of 'a open_faced_sandwich;

"... is not a type definition but a shape that represents";
"many different datatypes";

"So what is int open_faced_sandwich?";
"The simplest way of saying: An instance of the definition of";
"'a open_faced_sandwich;";
"... Where 'a stands for _int_";

"And waht is bool open_faced_sandwich";
"Much the same: An instance of the definition of";
"'a open_faced_sandwich;";
"... Where 'a stands for _boolean_";

"Does that also mean that we can derivce as many types as we";
"want from the shape";
"'a open_faced_sandwich";
"I guess it does yes";

"Is";
Bread(0);
"an open_faced_sandwich?";
"Indeed it is !";

"Why does it belong to";
"    int open_faced_sandwich";
"and not";
"    bool open_faced_sandwich";
"Because the shape of 'a is an int";

"and what is the type of";
Bread(true);
"It would figure that its a bool open_faced_sandwich";

"To what type does";
Bread(
  One_more_than(
  Zero));
"Belong ?";
"I reason it is a num open_faced_sandwich";

" o---- The First Moral ----o";
" Use datatype to describe types. When a type contains lots of";
" values, the datatype definition refers to itself. Use α ('a) ";
" with datatypes to define shapes";

(* vim: set ft=sml wrap: *)
