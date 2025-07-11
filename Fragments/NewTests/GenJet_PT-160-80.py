from GeneratorInterface.Core.generatorSmeared_cfi import generatorSmeared
from PhysicsTools.HepMCCandAlgos.genParticles_cfi import genParticles
from RecoJets.Configuration.GenJetParticles_cff import genParticlesForJets
from RecoJets.JetProducers.ak4GenJets_cfi import ak4GenJets
 
subleadSelector = cms.EDFilter("CandViewSelector",
    src = cms.InputTag("ak4GenJets"),
    cut = cms.string("pt > 80 & abs(eta) < 3.0")
)

leadSelector = cms.EDFilter("CandViewSelector",
    src = cms.InputTag("ak4GenJets"),
    cut = cms.string("pt > 160 & abs(eta) < 2.0")
)

subleadFilter = cms.EDFilter("CandViewCountFilter",
     src = cms.InputTag("subleadSelector"),
     minNumber = cms.uint32(2),
)

leadFilter = cms.EDFilter("CandViewCountFilter",
     src = cms.InputTag("leadSelector"),
     minNumber = cms.uint32(1),
) 
ProductionFilterSequence = cms.Sequence(generator*cms.SequencePlaceholder('VtxSmeared')*generatorSmeared*genParticles*genParticlesForJets*ak4GenJets*subleadSelector*leadSelector*subleadFilter*leadFilter)

