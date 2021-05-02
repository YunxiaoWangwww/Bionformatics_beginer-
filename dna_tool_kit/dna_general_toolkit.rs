use rand::Rng;
use regex::Regex;
fn _gen_random_seq(length: i32) -> String{ //pass an integer(i32) into the function as input (named length) and output will be a string
    let nucleotides = vec!['A','T','C','G'];
    let mut rnd_str = String::new(); //create an empty string 
    for _ in 0..length{ //to iterate between 0 and length 
        rnd_str.push(nucleotides[rand:: thread_rng().gen_range(0,nucleotides.len())]);
    //push the nucleotide into the empty string randomly -> rand:: thread_rng() is calling a random generator, to generate a random number from 0 to 4 (nucleotides list length) not include 4
    }
    return rnd_str;
}
fn _transcription(dna: &String) -> String{
    return dna.replace("T","U");
}
fn _reverse_complement(dna: &String) -> String { //immutable hashtable
    let trans_hashmap: HashMap<char, char> = [('A', 'T'), ('T', 'A'), ('C', 'G'), ('G','C')]
        .iter() //hashmap can be copied into a collection to be iterated 
        .copied()
        .collect();
    let mut complement_dna = String::new();
    for nuc in dna.chars().rev(){ //rev() is to return the reversed dna squence
        complement_dna.push(trans_hashmap[&nuc]);

    }
    return complement_dna;
}
//translation 
fn _dna_to_protein_hash_maps(dna: &String) -> String{
    let _dna_to_protein_hm: HashMap<&str,char> = [("ATA",'I'), ("ATC",'I'), ("ATT",'I'), ("ATG",'M'),("ACA",'T'), ("ACC",'T'), ("ACG",'T'), ("ACT",'T'),("AAC",'N'), ("AAT",'N'), ("AAA",'K'), ("AAG",'K'),("AGC",'S'), ("AGT",'S'), ("AGA",'R'), ("AGG",'R'),("CTA",'L'), ("CTC",'L'), ("CTG",'L'), ("CTT",'L'),("CCA",'P'), ("CCC",'P'), ("CCG",'P'), ("CCT",'P'),("CAC",'H'), ("CAT",'H'), ("CAA",'Q'), ("CAG",'Q'),("CGA",'R'), ("CGC",'R'), ("CGG",'R'), ("CGT",'R'),("GTA", 'V'), ("GTC",'V'), ("GTG",'V'), ("GTT",'V'),("GCA",'A'), ("GCC",'A'), ("GCG",'A'), ("GCT",'A'),("GAC",'D'), ("GAT",'D'), ("GAA",'E'), ("GAG",'E'),("GGA",'G'), ("GGC",'G'), ("GGG",'G'), ("GGT",'G'),("TCA",'S'), ("TCC", 'S'), ("TCG", 'S'), ("TCT",'S'),("TTC",'F'), ("TTT", 'F'), ("TTA",'L'), ("TTG",'L'),("TAC",'Y'), ("TAT",'Y'), ("TAA",'_'), ("TAG", '_'),("TGC", 'C'), ("TGT",'C'), ("TGA",'_'), ("TGG", 'W')]
        .iter() //hashmap can be copied into a collection to be iterated 
        .copied()
        .collect();
    let mut protein_string = String::new();
    for i in (0..(dna.chars().count()-2)).step_by(3){
        let dna_clone: String = dna.chars().collect::<Vec<_>>()[i..i+3].iter().cloned().collect::<String>();
        if _dna_to_protein_hm.contains_key(&*dna_clone){
            protein_string.push(_dna_to_protein_hm[&*dna_clone]);
        }
        else{
            protein_string.push('*');
        }
    }
    return protein_string;
}

fn _codon_usage(dna:&String, amino_acid:char) -> HashMap<String,f64> {
    let _dna_to_protein_hm: HashMap<&str,char> = [("ATA",'I'), ("ATC",'I'), ("ATT",'I'), ("ATG",'M'),("ACA",'T'), ("ACC",'T'), ("ACG",'T'), ("ACT",'T'),("AAC",'N'), ("AAT",'N'), ("AAA",'K'), ("AAG",'K'),("AGC",'S'), ("AGT",'S'), ("AGA",'R'), ("AGG",'R'),("CTA",'L'), ("CTC",'L'), ("CTG",'L'), ("CTT",'L'),("CCA",'P'), ("CCC",'P'), ("CCG",'P'), ("CCT",'P'),("CAC",'H'), ("CAT",'H'), ("CAA",'Q'), ("CAG",'Q'),("CGA",'R'), ("CGC",'R'), ("CGG",'R'), ("CGT",'R'),("GTA", 'V'), ("GTC",'V'), ("GTG",'V'), ("GTT",'V'),("GCA",'A'), ("GCC",'A'), ("GCG",'A'), ("GCT",'A'),("GAC",'D'), ("GAT",'D'), ("GAA",'E'), ("GAG",'E'),("GGA",'G'), ("GGC",'G'), ("GGG",'G'), ("GGT",'G'),("TCA",'S'), ("TCC", 'S'), ("TCG", 'S'), ("TCT",'S'),("TTC",'F'), ("TTT", 'F'), ("TTA",'L'), ("TTG",'L'),("TAC",'Y'), ("TAT",'Y'), ("TAA",'_'), ("TAG", '_'),("TGC", 'C'), ("TGT",'C'), ("TGA",'_'), ("TGG", 'W')]
    .iter() //hashmap can be copied into a collection to be iterated 
    .copied()
    .collect();
    let mut frequency_hm: HashMap<String,f64> = HashMap::new(); 
    let total_weight = ((Regex::new(&amino_acid.to_string()).unwrap()).find_iter(&_dna_to_protein_hash_maps(dna).to_string()).count())as f64;
    println!("{}", total_weight);
    for i in (0..(dna.chars().count()-2)).step_by(3){
        let dna_clone= dna.chars().collect::<Vec<_>>()[i..i+3].iter().cloned().collect::<String>();
        if (_dna_to_protein_hm.contains_key(&*dna_clone)) && (_dna_to_protein_hm[&*dna_clone] == amino_acid){
            if frequency_hm.contains_key(&*dna_clone){
                *frequency_hm.get_mut(&*dna_clone).unwrap() += 1.00/total_weight;
            }
            else{
                frequency_hm.insert(dna_clone, 1.00/total_weight);
            }
        }
    }
    return frequency_hm;
}

fn _gc_content(dna: &String) -> f64 {
    let gc_percentage = (dna.matches('C').count() as f64 + dna.matches('G').count() as f64)/(dna.chars().count() as f64);
    return gc_percentage;
}

fn _gen_reading_frames(dna:&String) -> Vec<String>{
    let mut gen_reading_frame: Vec<String> = Vec::new();
    gen_reading_frame.push(dna[0..].to_string());
    gen_reading_frame.push(dna[1..].to_string());
    gen_reading_frame.push(dna[3..].to_string());
    gen_reading_frame.push(_reverse_complement(&dna));
    gen_reading_frame.push(_reverse_complement(&dna[1..].to_string()));
    gen_reading_frame.push(_reverse_complement(&dna[2..].to_string()));
    return gen_reading_frame;
}

fn _all_posible_protein(dna:&str) -> Vec<String>{
    let protein_sequence = translate(dna.as_bytes());
    let mut current_prot: Vec<String> = Vec::new();
    let mut protein_prot: Vec<String> = Vec::new();
    for aa in protein_sequence.chars(){
        if aa == '*'{
            if true &current_prot.is_empty() == false{
                for p in &current_prot{
                    protein_prot.push(p.to_string());    
                }
                current_prot.clear();
            }
        }
        else{
            if aa == 'M'{
                &current_prot.push("".to_string());
            }
            for i in 0..current_prot.len(){
                &current_prot[i].push_str(&aa.to_string());
            }

        }
    }
    return protein_prot;
}

//print all possible proteins from a dna sequence (six open reading frames)
fn _all_orf_protein(dna:&str, start_read_pos:usize, end_read_pos:usize) -> Vec<String>{
    let mut all_orf_protein: Vec<String> = Vec::new();
    let mut _rfs: Vec<String> = Vec::new();
    if end_read_pos > start_read_pos{
        let tmp_seq : &str = &dna[start_read_pos..end_read_pos];
        _rfs = _gen_reading_frames(&tmp_seq.to_string());
    }
    for rf in _rfs{
        let prots: Vec<String> = _all_posible_protein(&rf);
        for p in prots{
            if all_orf_protein.contains(&p) == false{
                all_orf_protein.push(p.to_string());
            }
        }
    }
    all_orf_protein.sort_by(|l, r| Ord::cmp(&r.len(), &l.len()).then(Ord::cmp(l, r))); //sort the vector list according to the element string length, the longest element will be the first element in the vector list
    return all_orf_protein;
}


 
