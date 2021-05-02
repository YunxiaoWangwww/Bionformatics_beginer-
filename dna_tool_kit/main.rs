include!("dna_toolkit.rs");
use protein_translate::translate;

fn main() {
    println!("Hello, world!");
    _intro();
    _strings();
    let dna = String::from(_gen_random_seq(100));
    println!("{}",dna);
    println!("{}",_transcription(&dna));//by passing &, the loction of dna will be used instead of modifying dna directly
    _hash_maps();
    println!("{}", _reverse_complement(&"ATCG".to_string())); //"ATCG" need to be formated as a string structure to run this function
    println!("{}", _reverse_complement(&dna));
    println!("{}",translate(&dna.as_bytes()));
    println!("{}",_dna_to_protein_hash_maps(&dna));
    let map = _codon_usage(&dna,'L');
    for (key,value) in &map{
        println!("{}/{}",key,value);
    }
    println!("{}",_gc_content(&dna));
    for items in _gen_reading_frames(&dna){
        println!("{}",items);
    }
    for aa in _all_posible_protein(&dna){
        println!("{}",aa);
    }
    println!("{:?}",_all_orf_protein(&dna, 0,dna.chars().count()));
}
