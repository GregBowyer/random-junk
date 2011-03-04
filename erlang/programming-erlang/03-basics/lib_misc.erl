-module(lib_misc).
-export([for/3, pythag/1, odds_and_evens/1]).

for(Max, Max, F) -> [F(Max)];
for(I, Max, F)   -> [F(I) | for(I+1, Max, F)].

pythag(N) ->
    [ {A, B, C} ||
        A <- lists:seq(1, N),
        B <- lists:seq(1, N),
        C <- lists:seq(1, N),
        A+B+C =< N,
        (A*A) + (B*B) =:= (C*C)].

odds_and_evens(L) ->
    odds_and_evens_iter(L, [], []).

odds_and_evens_iter([Car | Cdr], Odds, Evens) ->
    case (Car rem 2) of
        1 -> odds_and_evens_iter(Cdr, [Car | Odds], Evens);
        0 -> odds_and_evens_iter(Cdr, Odds, [Car | Evens])
    end;
odds_and_evens_iter([], Odds, Evens) -> 
    {lists:reverse(Odds), lists:reverse(Evens)}.

