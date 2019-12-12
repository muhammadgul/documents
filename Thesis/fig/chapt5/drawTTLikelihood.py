#!/usr/bin/env python

import ROOT


if __name__ == '__main__':
    
    # Style settings
    ROOT.gStyle.SetHistMinimumZero(True)
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetStripDecimals(False)
    ROOT.TH1.SetDefaultSumw2(True)
    ROOT.TGaxis.SetMaxDigits(3)
    
    ROOT.gStyle.SetTitleFont(42)
    ROOT.gStyle.SetTitleFontSize(0.04)
    ROOT.gStyle.SetTitleFont(42, 'XYZ')
    ROOT.gStyle.SetTitleXOffset(1.0)
    ROOT.gStyle.SetTitleYOffset(1.1)
    ROOT.gStyle.SetTitleSize(0.045, 'XYZ')
    ROOT.gStyle.SetLabelFont(42, 'XYZ')
    ROOT.gStyle.SetLabelOffset(0.007, 'XYZ')
    ROOT.gStyle.SetLabelSize(0.04, 'XYZ')
    ROOT.gStyle.SetNdivisions(508, 'XYZ')
    
    ROOT.gROOT.ForceStyle()
    
    # Enable batch mode
    ROOT.gROOT.SetBatch(True)
    
    
    # Prepare for drawing
    canvas = ROOT.TCanvas('canvas', '', 1200, 900)
    canvas.SetRightMargin(0.15)
    canvas.SetTicks()
    
    
    inputFile = ROOT.TFile('TTRecoLikelihood_2016-pt20-v4.root')
    
    
    histOrig = inputFile.Get('mWhad_vs_mtophad_right')
    histOrig.SetDirectory(None)
    
    histReflected = ROOT.TH2D(
        'histReflected', ';Mass of t_{had} [GeV];Mass of W_{had} [GeV]',
        500, 0., 500., 300, 0., 300.
    )
    
    for binX in range(1, 301):
        for binY in range(1, 501):
            histReflected.SetBinContent(binY, binX, histOrig.GetBinContent(binX, binY))
    
    histReflected.Rebin2D()
    histReflected.Draw('colz')
    
    canvas.Print('M3.pdf')
    
    
    histDNu = inputFile.Get('nusolver_chi2_right')
    
    histDNu.SetTitle(';Minimal D_{#nu} [GeV];Probability density [GeV^{-1}]')
    histDNu.SetLineColor(ROOT.kAzure + 4)
    histDNu.SetFillColorAlpha(ROOT.kAzure + 5, 0.4)
    
    histDNu.Scale(1, 'width')
    
    histDNu.Draw('hist')
    canvas.SetRightMargin(0.1)
    canvas.Print('Dnu.pdf')
    
    inputFile.Close()

