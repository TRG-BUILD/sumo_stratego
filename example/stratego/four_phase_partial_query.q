//This file was generated from (Academic) UPPAAL 4.1.20-stratego-8-beta6 (rev. 2B32AEEE2ECD4B4F), January 2021


/*

*/
strategy opt = minE(Q) [<=HORIZON] {A[0], A[1], A[2], B[0], B[1], B[2], get_phase_id(is_active)}->{}:<>time>=HORIZON


/*

*/
simulate 1 [<=HORIZON] {get_phase_id(is_active)} under opt


