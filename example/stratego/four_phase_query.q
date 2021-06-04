//This file was generated from (Academic) UPPAAL 4.1.20-stratego-8-beta6 (rev. 2B32AEEE2ECD4B4F), January 2021


/*
strategy opt = minE(Q) [<=HORIZON]{Control.location}->{queueE, queueS, isP1}:<>time>=HORIZON \/\/ Broken due to collectPossibleIndex()::DOT
*/
strategy opt = minE(Q) [<=HORIZON]:<>time>=HORIZON


/*

*/
simulate 1 [<=HORIZON] {get_phase_id(is_active)} under opt


