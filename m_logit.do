clear all


import excel "E:\natalia\hc\dados_total.xlsx", sheet("Sheet1") firstrow

encode resultado, generate(c_result)
encode tipo_grupo_risco , generate(c_grupo_risco)
encode vga, generate(c_vga)
encode genero, generate(c_gen)
encode decisao_adpf_347, generate(c_347)
encode decisao_cnj_62, generate(c_cnj62)
encode coletividade, generate(c_col)

logit f_resultado grupo_risco resolucao_62 i.c_grupo_risco c_vga c_gen c_347
margins, dydx(grupo_risco resolucao_62 i.c_grupo_risco) post

logit f_resultado i.c_cnj62 i.c_vga i.c_gen i.c_347

logit indeferido recomendacao_62 recomendacao vga_roubo vga_homicidio vga_ameaca vga_lesao vga_est vga_latr vga_ext vga_seq vga_fem vga_abort vga_medida grupo_idosos grupo_hiv grupo_resp grupo_matern grupo_infecc grupo_imunossup grupo_doencas grupo_comorb grupo_lact grupo_hipert grupo_resp_menor grupo_resp_def indigenas adolescentes adpf_347
logit concedido recomendacao_62 recomendacao vga_roubo vga_homicidio vga_ameaca vga_lesao vga_est vga_latr vga_ext vga_seq vga_fem vga_abort vga_medida grupo_idosos grupo_hiv grupo_resp grupo_matern grupo_infecc grupo_imunossup grupo_doencas grupo_comorb grupo_lact grupo_hipert grupo_resp_menor grupo_resp_def indigenas adolescentes adpf_347
