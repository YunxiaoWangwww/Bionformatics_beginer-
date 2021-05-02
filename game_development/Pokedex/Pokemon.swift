import Foundation
struct PokemonList: Codable {
    let results: [Pokemon]
}
struct Pokemon: Codable {
    let name: String
    let url: String
}

struct PokemonData: Codable{
    let id: Int
    let types: [PokemonTypeEntry]
}

struct PokemonSprites: Codable{
    let name: String
    let sprites: SpriteInfo
}
struct SpriteInfo: Codable{
    let front_default: String
    let front_shiny:String
}

struct PokemonType: Codable{
    let name: String
    let url: String
}

struct PokemonTypeEntry: Codable{
    let slot: Int
    let type: PokemonType
}

struct PokemonCaught: Codable{
    var state = [String:Bool]()
}

struct PokemonSpecies: Codable{
    let flavor_text_entries: [speciestext]
}

struct speciestext: Codable {
    let flavor_text: String
    let language: language
}

struct language: Codable {
    let name: String
    let url: String
}


