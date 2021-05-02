//
//  NoteViewController.swift
//  Notes
//
//  Created by MaC on 03/12/2020.
//

import UIKit

class NoteViewController: UIViewController {
    var note: Note!
    @IBOutlet var textView: UITextView!
    override func viewDidLoad() {
        super.viewDidLoad()
        textView.text = note.contents
    }
    override func viewWillDisappear(_ animated: Bool) {
        super.viewWillDisappear(animated)
        note.contents = textView.text
        NoteManager.main.save(note: note)
    }
    
    
}
