library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity nott is
    port(
        clock : in std_logic;
        entrada : in std_logic_vector(7 downto 0);
        saida : out std_logic_vector(7 downto 0) 
    );
end entity;

architecture behavior of nott is
begin
    process(clock)
    begin
        if rising_edge(clock) then
            saida <= not(entrada);
        end if;
    end process;
end architecture;