-module(geomtry).
-export([start/0, area/2]).

square(N) -> N * N.
rectangle_area(Width, Height) -> Width * Height.
circle_area(R) ->  3.141592 * square(R).

start() -> spawn(fun loop/0).

loop() ->
    receive
        {From, {rectangle, Width, Height}} -> 
            Area = rectangle_area(Width, Height),
            io:format("Area of a Rectangle is ~p~n", [Area]),
            From ! {self(), Area},
            loop();
        {From, {circle, R}} ->
            Area = circle_area(R),
            io:format("Area of a circle is ~p~n", [Area]),
            From ! {self(), Area},
            loop();
        {From, Other} ->
            io:format("Burp ~n"),
            From ! {self(), {error, Other}},
            loop()
end.

area(Pid, Request) ->
    Pid ! {self(), Request},
    receive
        {Pid, Response} -> Response
end.

% Create the process with a spawn
% Pid = spawn(fun geomtry0:loop/0).
% Message it 
% Pid ! {rectangle, 6, 10}
