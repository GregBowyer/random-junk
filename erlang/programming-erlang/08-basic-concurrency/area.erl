-module(area).
-export([loop/0]).

square(N) -> N * N.
rectangle_area(Width, Height) -> Width * Height.
circle_area(R) ->  3.141592 * square(R).

loop() ->
    receive
        {rectangle, Width, Height} -> 
            Area = rectangle_area(Width, Height),
            io:format("Area of a Rectangle is ~p~n", [Area]),
            loop();
        {circle, R} ->
            Area = circle_area(R),
            io:format("Area of a circle is ~p~n", [Area]),
            loop();
        Other ->
            io:format("Burp ~n"),
            loop()
end.

% Create the process with a spawn
% Pid = spawn(fun geomtry0:loop/0).
% Message it 
% Pid ! {rectangle, 6, 10}
