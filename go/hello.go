package main

import "fmt"

func main() {
    // Go is a bit nicer on printf ?
    fmt.Printf("Hello from go\n")
    fmt.Printf("Hello from go %s\n", "wibble")
    fmt.Printf("Hello from go %s\n", new(World))
}

type World struct{}

func (w *World) String() string {
    return "wobble"
}
