//
//  ViewController.swift
//  Fiftygram
//
//  Created by MaC on 22/11/2020.
//

import UIKit

class ViewController: UIViewController, UIImagePickerControllerDelegate, UINavigationControllerDelegate {
    let context = CIContext()
    var original: UIImage?
    @IBOutlet var imageView: UIImageView!
    @IBAction func applySepia() {
        if original == nil {
            return
        }
        let filter = CIFilter(name: "CISepiaTone")
        filter?.setValue(0.5, forKey: kCIInputIntensityKey)
        display(filter: filter!)
    }
    @IBAction func applyToneCurve(){
        if original == nil {
            return
        }
        let filter = CIFilter(name:
            "CIToneCurve")
        
        let input0 = CIVector(x: 0.6,y: 0.0)
        let input1 = CIVector(x:0.4, y: 0.25)
        let input2 = CIVector(x: 0.5, y: 0.5)
        let input3 = CIVector(x: 0.75, y: 0.75)
        let input4 = CIVector(x: 1.0, y:1.0)
        filter?.setValue(input0, forKey: "inputPoint0")
        filter?.setValue(input1, forKey: "inputPoint1")
        filter?.setValue(input2, forKey: "inputPoint2")
        filter?.setValue(input3, forKey: "inputPoint3")
        filter?.setValue(input4, forKey: "inputPoint4")
        display(filter: filter!)
        
    }
    @IBAction func applyToneDull(){
        if original == nil {
            return
        }
        let filter = CIFilter(name: "CISRGBToneCurveToLinear")
        display(filter: filter!)
    }

    @IBAction func applyNoir(){
        if original == nil {
            return
        }
        let filter = CIFilter(name: "CIPhotoEffectNoir")
        display(filter: filter!)
    }
    @IBAction func applyVintage(){
        if original == nil{
            return
        }
        let filter = CIFilter(name: "CIPhotoEffectProcess")
        display(filter: filter!)
    }
    @IBAction func save(){
        if imageView.image == nil{
            return
        }
        UIImageWriteToSavedPhotosAlbum(imageView.image!, nil, nil, nil)
        let alertController = UIAlertController(title: "Fiftygram", message:
            "Photo saved", preferredStyle: .alert)
        alertController.addAction(UIAlertAction(title: "Dismiss", style: .default))
        self.present(alertController, animated: true, completion: nil)

    }
    
    func display(filter: CIFilter){
        filter.setValue(CIImage(image: original!), forKey: kCIInputImageKey)
        let output = filter.outputImage
        let cgImage = self.context.createCGImage(output!, from: output!.extent)!
        imageView.image = UIImage(cgImage: cgImage, scale: 1.0, orientation: original!.imageOrientation)
    }
    @IBAction func choosePhoto (){
        if UIImagePickerController.isSourceTypeAvailable(.photoLibrary){
            let picker = UIImagePickerController()
            picker.delegate = self
            picker.sourceType = .photoLibrary
            navigationController?.present(picker, animated: true, completion: nil)
        }
    }
    func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [UIImagePickerController.InfoKey : Any]) {
        navigationController?.dismiss(animated: true, completion: nil)
        if let image = info[UIImagePickerController.InfoKey.originalImage] as? UIImage{
            imageView.image = image
            original = image
        }

    }
}

