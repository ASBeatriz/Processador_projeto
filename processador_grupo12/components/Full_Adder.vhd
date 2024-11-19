library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity Full_Adder is
    port(
        A, B, Cin : in std_logic;
        S, Cout : out std_logic
    );
end entity;

architecture behavior of Full_Adder is
begin

    S <= A xor B xor Cin;
    cout <= (A and B) or (A and Cin) or (B and Cin);
    
end architecture;