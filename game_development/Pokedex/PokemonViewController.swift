import UIKit
class PokemonViewController: UIViewController{
    @IBOutlet var nameLabel: UILabel!
    @IBOutlet var numberLabel: UILabel!
    @IBOutlet var type1Label: UILabel!
    @IBOutlet var type2Label: UILabel!
    @IBOutlet var catchpokemon: UIButton!
    @IBOutlet var pokemonpicture: UIImageView!
    @IBOutlet var pokemondescription: UILabel!
    var pokemon: Pokemon!
    var catched = true
    var pokemoncaught = PokemonCaught.init(state: [ : ])
    var specieslist: [String] = []


    override func viewDidLoad() {
        super.viewDidLoad()
        type1Label.text = ""
        type2Label.text = ""
        pokemondescription.text = ""
        let url = URL(string: pokemon.url)
        guard let u = url else{
            return
        }
    
        URLSession.shared.dataTask(with: u) { (data, response, error) in
            guard let data = data else{
                return
            }
            do{
                let pokemonData = try JSONDecoder().decode(PokemonData.self, from: data)
                let pokemonSprites = try JSONDecoder().decode(PokemonSprites.self, from: data)
                DispatchQueue.main.async{
                    self.nameLabel.text = self.pokemon.name
                    self.numberLabel.text = String(format: "#%03d", pokemonData.id)

                    if UserDefaults.standard.bool(forKey: self.nameLabel.text!) == false {
                        self.catchpokemon.setTitle("Catch", for: .normal)
                    }
                    else{
                        self.catchpokemon.setTitle("Release", for: .normal)
                    }
                    
                    for typeEntry in pokemonData.types{
                        if typeEntry.slot == 1{
                            self.type1Label.text = typeEntry.type.name
                        }
                        else if typeEntry.slot == 2{
                            self.type2Label.text = typeEntry.type.name
                        }
                    }
                    let spriteURL = URL(string: pokemonSprites.sprites.front_default)
                    let pokeSprites = try?Data(contentsOf: spriteURL!)
                    self.pokemonpicture.image = UIImage(data: pokeSprites!)
                    
                    
                    let urlspecies = URL(string: "https://pokeapi.co/api/v2/pokemon-species/" + String(pokemonData.id) + "/")
                    guard let urlSpecies = urlspecies else{
                        return
                    }
    
                    URLSession.shared.dataTask(with: urlSpecies) { (data, response, error) in
                        guard let dataspecies = data else{
                            return
                        }
                        do{
                            let pokemonSpecies = try JSONDecoder().decode(PokemonSpecies.self, from: dataspecies)
                            DispatchQueue.main.async{
                                for species in pokemonSpecies.flavor_text_entries {
                                    if species.language.name == "en"{
                                        self.pokemondescription.text = String(species.flavor_text)
                                    }
                                    
                                }
                            }
                        }
                        catch let error {
                            print("\(error)")
                        }
                    }.resume()
                    
                }
            }
            catch let error {
                print("\(error)")
            }
        }.resume()
    }
    @IBAction func toggleCatch() {
        if catched && pokemoncaught.state[nameLabel.text!] == nil || pokemoncaught.state[nameLabel.text!] == false {
            catchpokemon.setTitle("Release", for: UIControl.State.normal)
            catched = false
            pokemoncaught.state[nameLabel.text!] = true
            UserDefaults.standard.set(true, forKey: nameLabel.text!)
        }
        else {
            catchpokemon.setTitle("Catch", for: UIControl.State.normal)
            catched = true
            pokemoncaught.state[nameLabel.text!] = false
            UserDefaults.standard.set(false,forKey: nameLabel.text!)
        }
        
    }
}


