c d   " / D i o m e d e s / D a t a "  
  
  
 i m p o r t - m o d u l e   A c t i v e D i r e c t o r y  
  
 $ c u r r e n t D a t e   =   G e t - D a t e   - f o r m a t   " M M - d d - y y "    
 $ f i l e N a m e   =   ( " D i o m e d e s N o n R e c u r s i v e G r o u p s DOMAINNAME_ "   +   $ c u r r e n t D a t e   +   " . c s v " )  
  
 #   A M S   i s   a   o r g a n i z a t i o n a l   u n i t   o f   t h e   r o o t   d o m a i n  
 $ G r o u p s   =   ( G e t - A d G r o u p   - f i l t e r   *   - S e r v e r   " ROOTDOMAIN"   - s e a r c h b a s e   " O U =?, D C =?, D C =?" |   W h e r e   { $ _ . n a m e   - l i k e   " * * " }   |   s e l e c t   n a m e   - E x p a n d P r o p e r t y   n a m e )  
  
 $ T a b l e   =   @ ( )  
  
 $ R e c o r d   =   @ {  
     " G r o u p   N a m e "   =   " "  
     " N a m e "   =   " "  
     " U s e r n a m e "   =   " "  
     " C o m p a n y "   =   "COMPANYNAME"      
 }  
  
  
 F o r e a c h   ( $ G r o u p   i n   $ G r o u p s )   {  
  
     $ A r r a y o f m e m b e r s   =   G e t - A D G r o u p M e m b e r     - S e r v e r   " ROOTDOMAIN"   - i d e n t i t y   $ G r o u p   |   s e l e c t   n a m e , s a m a c c o u n t n a m e  
  
     f o r e a c h   ( $ M e m b e r   i n   $ A r r a y o f m e m b e r s )   {  
         $ R e c o r d . " G r o u p   N a m e "   =   $ G r o u p  
         $ R e c o r d . " N a m e "   =   $ M e m b e r . n a m e  
         $ R e c o r d . " U s e r N a m e "   =   $ M e m b e r . s a m a c c o u n t n a m e  
         $ o b j R e c o r d   =   N e w - O b j e c t   P S O b j e c t   - p r o p e r t y   $ R e c o r d  
         $ T a b l e   + =   $ o b j r e c o r d  
  
     }  
 }  
  
 $ T a b l e   |   e x p o r t - c s v   $ f i l e N a m e   - N o T y p e I n f o r m a t i o n  
  
 # h t t p s : / / s e r v e r f a u l t . c o m / q u e s t i o n s / 5 3 2 9 4 5 / l i s t - a l l - g r o u p s - a n d - t h e i r - m e m b e r s - w i t h - p o w e r s h e l l - o n - w i n 2 0 0 8 r 2
