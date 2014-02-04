{

	Int_t nBin = 36;
	Int_t uprLim = 170;
	Int_t lwrLim = 80;
	
	// preliminary information
	TString dir11 = "C:/Users/ryanrp/Documents/CERN/analysis/ZZ_rpetersburg/allData/";
	TString dir12 = dir11;

	TString baseSaveName = "lowMass";
	Bool_t doRed = true;

	if(!doRed) baseSaveName += "_noZJets";

	const int nChannel = 4;
	TString hTree [nChannel] = {"tree_incl_4mu", "tree_incl_2mu2e", "tree_incl_2e2mu", "tree_incl_4e"};
	TString chLatex[nChannel] = {"4#mu", "2#mu2e", "2e2#mu", "4e"};

	// Background 
	const int nZZBkgFile = 2; // Basically the year
	// ZZ files		
	TString zzBkgFileName[nZZBkgFile] = {dir11+"mc11_ZZComb.root", dir12+"mc12_ZZComb.root"};

	//Reading the file
	TFile *zzBkgFile[nZZBkgFile];
	for(Int_t i=0; i<nZZBkgFile; i++){
		zzBkgFile[i] = new TFile(zzBkgFileName[i],"Read");
	}

	TH1F ***zzBkgHistYearCh = NULL;
	TH1F **zzBkgHistYear = NULL;
	TH1F **zzBkgHistCh = NULL;
	TH1F *zzBkgHist = NULL;
	//fillHistogram(nZZBkgFile, zzBkgFile, nChannel, hTree, "zzBKG",zzBkgHistYearCh, zzBkgHistYear,zzBkgHistCh, zzBkgHist);
	
	TString baseName = "zzBKG";
	
	
	
	// Reading the trees
	zzBkgHist = new TH1F(baseName, baseName, nBin, lwrLim, uprLim);

	// initializing the histograms...
	zzBkgHistYearCh = new TH1F** [nZZBkgFile];
	zzBkgHistYear = new TH1F* [nZZBkgFile];
	for(Int_t i = 0; i < nZZBkgFile; i++)
	{
		zzBkgHistYear[i] = new TH1F(baseName+"year"+TString::Itoa(i,10), baseName+"year"+TString::Itoa(i,10), nBin, lwrLim, uprLim);
		// Another step in init the hist.
		zzBkgHistYearCh[i] = new TH1F* [nChannel];

		for(Int_t j = 0; j < nChannel; j++)
		{
			cout<<baseName<<" i: "<<i<<" j: "<<j<<endl;
			zzBkgHistYearCh[i][j] = new TH1F(baseName+"yearCH"+TString::Itoa(i,10)+hTree[j], baseName+"yearCH"+TString::Itoa(i,10)+hTree[j], nBin, lwrLim, uprLim);
			// Reading the tree
			TTree *currTree = (TTree *) zzBkgFile[i]->Get(hTree[j]);

			currTree->Draw("m4l_constrained>>"+baseName+"yearCH"+TString::Itoa(i,10)+hTree[j], "weight");
			//currTree->Draw("m4l_constrained","weight");
			
			zzBkgHistYear[i]->Add(zzBkgHistYearCh[i][j]);
			zzBkgHist->Add(zzBkgHistYearCh[i][j]);
		}
	}
	zzBkgHistCh = new TH1F* [nChannel];

	for(Int_t i = 0; i < nChannel; i++)
	{
		zzBkgHistCh[i] = new TH1F(baseName+"CH"+hTree[i], baseName+"CH"+hTree[i], nBin, lwrLim, uprLim);
		for(Int_t j = 0; j< nZZBkgFile; j++)
		{
			zzBkgHistCh[i]->Add(zzBkgHistYearCh[j][i]);
		}
	}

		
}