#!/usr/bin/env python

"""Plots signal cross section as a function of mA with uncertainties.

Cross sections are read from file Spin0_xsecs_vs_mass_MG260.root
from [1].  Select only CP-odd state with a 10% width, l+jets final
state.

[1] https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTTBar#Data_and_simulated_samples
"""


import ROOT


if __name__ == '__main__':
    
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
    
    ROOT.gROOT.SetBatch(True)
    
    
    canvas = ROOT.TCanvas('canvas', '', 1200, 900)
    canvas.SetTicks()
    
    
    inputFile = ROOT.TFile('Spin0_xsecs_vs_mass_MG260.root')
    
    for diag in ['res', 'int']:
        
        prefix = 'pp_a0_{}_SL_w10_'.format(diag.upper())
        graphTotalUnc = inputFile.Get(prefix + 'toterr')
        graphPDFUnc = inputFile.Get(prefix + 'pdferr')
        graphRenormUp = inputFile.Get(prefix + 'muRhi')
        graphRenormDown = inputFile.Get(prefix + 'muRlo')
        graphFactorUp = inputFile.Get(prefix + 'muFhi')
        graphFactorDown = inputFile.Get(prefix + 'muFlo')
        
        
        graphNominal = ROOT.TGraph(graphTotalUnc)
        
        graphRenormUnc = ROOT.TGraphAsymmErrors(graphNominal.GetN())
        x, y = ROOT.Double(), ROOT.Double()
        
        for i in range(graphRenormUnc.GetN()):
            graphNominal.GetPoint(i, x, y)
            graphRenormUnc.SetPoint(i, x, y)
            yNominal = float(y)
            graphRenormUp.GetPoint(i, x, y)
            yUp = float(y)
            graphRenormDown.GetPoint(i, x, y)
            yDown = float(y)
            graphRenormUnc.SetPointError(i, 0., 0., yUp - yNominal, yNominal - yDown)
        
        graphFactorUnc = ROOT.TGraphAsymmErrors(graphNominal.GetN())
        
        for i in range(graphFactorUnc.GetN()):
            graphNominal.GetPoint(i, x, y)
            graphFactorUnc.SetPoint(i, x, y)
            yNominal = float(y)
            graphFactorUp.GetPoint(i, x, y)
            yUp = float(y)
            graphFactorDown.GetPoint(i, x, y)
            yDown = float(y)
            graphFactorUnc.SetPointError(i, 0., 0., yUp - yNominal, yNominal - yDown)
        
        
        graphTotalUnc.SetTitle(';m_{#Phi} [GeV];Cross section [pb]')
        graphTotalUnc.SetFillColorAlpha(ROOT.kWhite, 0.)
        graphTotalUnc.Draw('a3')
        graphTotalUnc.GetXaxis().SetLimits(400., 750.)
        
        graphRenormUnc.SetFillColorAlpha(ROOT.kAzure + 5, 0.5)
        graphRenormUnc.SetLineColorAlpha(ROOT.kAzure + 5, 0.5)
        graphRenormUnc.Draw('3')
        
        graphFactorUnc.SetFillColorAlpha(ROOT.kRed + 1, 0.5)
        graphFactorUnc.SetLineColorAlpha(ROOT.kRed + 1, 0.5)
        graphFactorUnc.Draw('3')
        
        graphPDFUnc.SetFillColorAlpha(ROOT.kGreen + 1, 0.5)
        graphPDFUnc.SetLineColorAlpha(ROOT.kGreen + 1, 0.5)
        graphPDFUnc.Draw('3')
        
        graphNominal.SetLineColor(ROOT.kBlack)
        graphNominal.Draw('l')
        
        
        if diag == 'res':
            legend = ROOT.TLegend(0.65, 0.85 - 0.04 * 5, 0.65 + 0.25, 0.85)
            legend.SetHeader('#font[62]{A, 10%, res.}')
        else:
            legend = ROOT.TLegend(0.65, 0.65 - 0.04 * 5, 0.65 + 0.25, 0.65)
            legend.SetHeader('#font[62]{A, 10%, int.}')
        
        legend.SetFillColorAlpha(ROOT.kWhite, 0.)
        legend.SetBorderSize(0)
        legend.SetTextFont(42)
        legend.SetTextSize(0.035)
        
        legend.AddEntry(graphNominal, ' Nominal ', 'l')
        legend.AddEntry(graphRenormUnc, ' #mu_{R} unc. ', 'f')
        legend.AddEntry(graphFactorUnc, ' #mu_{F} unc. ', 'f')
        legend.AddEntry(graphPDFUnc, ' PDF unc. ', 'f')
        
        legend.Draw()
        
        
        canvas.RedrawAxis()
        canvas.Print('crossSectionUnc_{}.pdf'.format(diag))
        
        
        print('Relative total uncertainty, {}:'.format(diag))
        
        for i in range(graphTotalUnc.GetN()):
            graphTotalUnc.GetPoint(i, x, y)
            yNominal = float(y)
            print('  {:0.3f}'.format(graphTotalUnc.GetErrorY(i) / yNominal))
        
        print()
    
    inputFile.Close()
