male("George").
male("Spencer").
male("Philip").
male("Charles").
male("Mark").
male("Andrew").
male("Edward").
male("William").
male("Harry").
male("Peter").
male("James").


female("Mum").
female("Kydd").
female("Elizabeth").
female("Margaret").
female("Diana").
female("Anne").
female("Sarah").
female("Sophie").
female("Zara").
female("Beatrice").
female("Eugenie").
female("Louise").


spouse_to("George", "Mum").
spouse_to("Spencer", "Kydd").
spouse_to("Elizabeth", "Philip").
spouse_to("Diana", "Charles").
spouse_to("Anne", "Mark").
spouse_to("Andrew", "Sarah").
spouse_to("Edward","Sophie").


child("Elizabeth", "George").
child("Elizabeth", "Mum").

child("Margaret", "George").
child("Margaret", "Mum").

child("Charles", "Elizabeth").
child("Charles", "Philip").

child("Anne", "Elizabeth").
child("Anne", "Philip").

child("Andrew", "Elizabeth").
child("Andrew", "Philip").

child("Edward", "Elizabeth").
child("Edward", "Philip").

child("Diana", "Spencer").
child("Diana", "Kydd").

child("William", "Diana").
child("William", "Charles").

child("Harry", "Diana").
child("Harry", "Charles").

child("Zara", "Anne").
child("Zara", "Mark").

child("Peter", "Anne").
child("Peter", "Mark").

child("Beatrice", "Andrew").
child("Beatrice", "Sarah").

child("Eugenie", "Andrew").
child("Eugenie", "Sarah").

child("Louise", "Edward").
child("Louise", "Sophie").

child("James", "Edward").
child("James", "Sophie").


sibling_to("Elizabeth", "Margaret").
sibling_to("Anne", "Charles").
sibling_to("Andrew", "Charles").
sibling_to("Edward", "Charles").
sibling_to("Andrew", "Anne").
sibling_to("Edward", "Anne").
sibling_to("Andrew", "Edward").
sibling_to("William", "Harry").
sibling_to("Zara", "Peter").
sibling_to("Beatrice", "Eugenie").
sibling_to("James", "Louise").


grandchild(A, B):-
	child(X, A),
	child(B, X).

grandparent(A,B):-
	child(A, X),
	child(X, B).

ancestor(A, B):-
	child(A, B);
	child(A, X),
	ancestor(X, B).

sibling(A, B):-
	sibling_to(A, B);
	sibling_to(B, A).

brother(A, B):-
	male(A),
	sibling(A, B).

sister(A, B):-
	female(B),
	sibling(A, B).

daughter(A, B):-
	female(A),
	child(A, B).

son(A, B):-
	male(A),
	child(A, B).

firstcousin(A, B):-
	child(A, X),
	child(X, Y),
	child(Z, Y),
	child(B, Z).

spouse(A, B):-
	spouse_to(A, B);
	spouse_to(B, A).

brotherinlaw(A, B):-
	spouse(A, X),
	brother(X , B).

brotherinlaw(A, B):-
	male(A),
	spouse(A, X),
	sibling(X, B).

brotherinlaw(A, B):-
	male(A),
	male(B),
	spouse(A, X),
	spouse(B, Y),
	sibling(X, Y).

brotherinlaw(A, B):-
	male(A),
	spouse(A, X),
	spouse(B, Y),
	sibling(X, Y).

sisterinlaw(A, B):-
	spouse(A, X),
	brother(X , B).

sisterinlaw(A, B):-
	female(A),
	spouse(A, X),
	sibling(X, B).

sisterinlaw(A, B):-
	female(A),
	female(B),
	spouse(A, X),
	spouse(B, Y),
	sibling(X, Y).

sisterinlaw(A, B):-
	female(A),
	spouse(A, X),
	spouse(B, Y),
	sibling(X, Y).

aunt(A, B):-
	child(A, X),
	female(B),
	sibling(B, X).

aunt(A, B):-
	child(A, X),
	sibling(Y, X),
	female(B),
	spouse(Y, B).

uncle(A, B):-
	child(A, X),
	male(B),
	sibling(B, X).

uncle(A, B):-
	child(A, X),
	sibling(Y, X),
	male(B),
	spouse(Y, B).

greatgrandparents(A, B):-
	child(A, X),
	child(X, Y),
	child(Y, B).
	

grandchildrenlist(X):-
	setof(Y, grandchild(X,Y),List),
	format("~w",[List]).

brothersinlaw(X):-
	setof(Y, brotherinlaw(X, Y), List),
	format("~w", [List]).

printgreatgrandparents(X):-
	setof(Y, greatgrandparents(X,Y),List),
	format("~w",[List]).

ancestors(X):-
	setof(Y, ancestor(X, Y),List),
	format("~w",[List]).