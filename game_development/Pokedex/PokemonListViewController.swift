import UIKit

class PokemonListViewController: UITableViewController, UISearchBarDelegate{
    @IBOutlet weak var searchBar: UISearchBar!
    var pokemon: [Pokemon] = []
    var filteredData: [Pokemon]!
    func captalize(text: String) -> String{
        return text.prefix(1).uppercased() + text.dropFirst()
    }
    override func viewDidLoad() {
        super.viewDidLoad()
        let url = URL(string: "https://pokeapi.co/api/v2/pokemon?limit=151")
        guard let u = url else{
            return
        }
        URLSession.shared.dataTask(with: u) { (data, response, error) in
            guard let data = data else{
                return
            }
            do{
                let pokemonList = try JSONDecoder().decode(PokemonList.self, from: data)
                self.pokemon = pokemonList.results
                DispatchQueue.main.async {
                    self.tableView.reloadData()
                }
            }
            catch let error {
                print("\(error)")
            }
        }.resume()
        searchBar.delegate = self
        filteredData = pokemon
        
        
    }
    override func numberOfSections(in tableView: UITableView) -> Int {
        return 1
    }
    override func tableView(_ tableView:UITableView, numberOfRowsInSection section:Int) -> Int{
            return filteredData.count
    }
    override func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "PokemonCell", for: indexPath)
        cell.textLabel?.text = captalize(text: filteredData[indexPath.row].name)
        return cell
    }
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        if segue.identifier == "PokemonSegue"{
            if let destination = segue.destination as? PokemonViewController{
                destination.pokemon = filteredData[tableView.indexPathForSelectedRow!.row]
            }
            
        }
    }
    func searchBar(_ searchBar: UISearchBar, textDidChange searchText: String) {
        filteredData = []
        if searchText == "" {
            filteredData = pokemon
            self.tableView.reloadData()
        }
        else{
            for pokemon in pokemon{
                if pokemon.name.lowercased().contains(searchText.lowercased()){
                    filteredData.append(pokemon)
                }
            }
            self.tableView.reloadData()
        }
    }
    
}



