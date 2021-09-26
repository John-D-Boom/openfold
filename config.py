import copy
import ml_collections as mlc


def model_config(name):
    c = copy.deepcopy(config)
    if(name == "model_3"):
        c.model.template.enabled = False
    elif(name == "model_4"):
        c.model.template.enabled = False
    elif(name == "model_5"):
        c.model.template.enabled = False
    
    return c
        

c_z = mlc.FieldReference(128)
c_m = mlc.FieldReference(256)
c_t = mlc.FieldReference(64)
c_e = mlc.FieldReference(64)
c_s = mlc.FieldReference(384)
blocks_per_ckpt = mlc.FieldReference(1)
chunk_size = mlc.FieldReference(4)#1280)
aux_distogram_bins = mlc.FieldReference(64)

config = mlc.ConfigDict({
    "model": {
        "c_z": c_z,
        "c_m": c_m,
        "c_t": c_t,
        "c_e": c_e,
        "c_s": c_s,
        "no_cycles": 4,
        "_mask_trans": False,
        "input_embedder": {
            "tf_dim": 22,
            "msa_dim": 49,
            "c_z": c_z,
            "c_m": c_m,
            "relpos_k": 32,
        },
        "recycling_embedder": {
            "c_z": c_z,
            "c_m": c_m, 
            "min_bin": 3.25,
            "max_bin": 20.75,
            "no_bins": 15,
            "inf": 1e8,
        },
        "template": {
            "distogram": {
                "min_bin": 3.25,
                "max_bin": 50.75,
                "no_bins": 39,
            },
            "template_angle_embedder": {
                # DISCREPANCY: c_in is supposed to be 51.
                "c_in": 57,
                "c_out": c_m,
            },
            "template_pair_embedder": {
                "c_in": 88,
                "c_out": c_t,
            },
            "template_pair_stack": {
                "c_t": c_t, 
                # DISCREPANCY: c_hidden_tri_att here is given in the supplement
                # as 64. In the code, it's 16.
                "c_hidden_tri_att": 16, 
                "c_hidden_tri_mul": 64,
                "no_blocks": 2, 
                "no_heads": 4, 
                "pair_transition_n": 2, 
                "dropout_rate": 0.25,
                "blocks_per_ckpt": blocks_per_ckpt,
                "chunk_size": chunk_size,
            },
            "template_pointwise_attention": {
                "c_t": c_t, 
                "c_z": c_z, 
                # DISCREPANCY: c_hidden here is given in the supplement as 64.
                # It's actually 16.
                "c_hidden": 16, 
                "no_heads": 4,
                "chunk_size": chunk_size,
            },
            "eps": 1e-6,
            "enabled": True,
            "embed_angles": True,
        },
        "extra_msa": {
            "extra_msa_embedder": {
                "c_in": 25,
                "c_out": c_e,
            },
            "extra_msa_stack": {
                "c_m": c_e,
                "c_z": c_z,
                "c_hidden_msa_att": 8,
                "c_hidden_opm": 32,
                "c_hidden_mul": 128,
                "c_hidden_pair_att": 32,
                "no_heads_msa": 8,
                "no_heads_pair": 4,
                "no_blocks": 4,
                "transition_n": 4,
                "msa_dropout": 0.15,
                "pair_dropout": 0.25,
                "blocks_per_ckpt": blocks_per_ckpt,
                "chunk_size": chunk_size,
                "inf": 1e9,
                "eps": 1e-10,
            },
            "enabled": True,
        },
        "evoformer_stack": {
            "c_m": c_m,
            "c_z": c_z,
            "c_hidden_msa_att": 32,
            "c_hidden_opm": 32,
            "c_hidden_mul": 128,
            "c_hidden_pair_att": 32,
            "c_s": c_s,
            "no_heads_msa": 8,
            "no_heads_pair": 4,
            "no_blocks": 48,
            "transition_n": 4,
            "msa_dropout": 0.15,
            "pair_dropout": 0.25,
            "blocks_per_ckpt": blocks_per_ckpt,
            "chunk_size": chunk_size,
            "inf": 1e9,
            "eps": 1e-10,
        },
        "structure_module": {
            "c_s": c_s, 
            "c_z": c_z,
            "c_ipa": 16,
            "c_resnet": 128,
            "no_heads_ipa": 12,
            "no_qk_points": 4,
            "no_v_points": 8,
            "dropout_rate": 0.1,
            "no_blocks": 8,
            "no_transition_layers": 1,
            "no_resnet_blocks": 2,
            "no_angles": 7,
            "trans_scale_factor": 10,
            "epsilon": 1e-12,
            "inf": 1e5,
        },
        "heads": {
            "lddt": {
                "no_bins": 50,
                "c_in": c_s,
                "c_hidden": 128,
            },
            "distogram": {
                "c_z": c_z,
                "no_bins": aux_distogram_bins,
            },
            "tm_score": {
                "c_z": c_z,
                "no_bins": aux_distogram_bins,
                "enabled": False,
            },
            "masked_msa": {
                "c_m": c_m,
                "c_out": 23,
            },
            "experimentally_resolved": {
                "c_s": c_s,
                "c_out": 37,
            },
        },
    },
    "relax": {
        "max_iterations": 0, # no max
        "tolerance": 2.39,
        "stiffness": 10.0,
        "max_outer_iterations": 20,
        "exclude_residues": [],
    },
    "loss": {
        "distogram": {
            "min_bin": 2.3125, 
            "max_bin": 21.6875, 
            "no_bins": 64, 
            "eps": 1e-6,
            "weight": 0.3, 
        },
        "experimentally_resolved": {
            "eps": 1e-8,
            "min_resolution": 0.1,
            "max_resolution": 3.0,
            "weight": 0.,
        },
        "fape": {
            "backbone": { 
                "clamp_distance": 10.,
                "loss_unit_distance": 10.,
                "weight": 0.5,
            },
            "sidechain": {
                "clamp_distance": 10.,
                "length_scale": 10.,
                "weight": 0.5,
            },
            "weight": 1.0,
        },
        "lddt": {
            "min_resolution": 0.1,
            "max_resolution": 3.0,
            "cutoff": 15.,
            "no_bins": 50,
            "eps": 1e-10,
            "weight": 0.01,
        },
        "masked_msa": {
            "eps": 1e-8,
            "weight": 2.0,
        },
        "supervised_chi": {
            "chi_weight": 0.5,
            "angle_norm_weight": 0.01,
            "eps": 1e-6,
            "weight": 1.0,
        },
        "violation": {
            "violation_tolerance_factor": 12.0,
            "clash_overlap_tolerance": 1.5,
            "eps": 1e-6,
            "weight": 0.,
        },
    },
})
