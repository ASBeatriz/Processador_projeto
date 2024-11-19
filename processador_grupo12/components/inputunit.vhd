library IEEE;
use IEEE.STD_LOGIC_1164.ALL;


--perguntar do clock para o aluno PAE, precisa de um clock e um enable?
entity inputunit is
    port(
        readbits : in std_logic_vector(7 downto 0);
        storebits : out std_logic_vector(7 downto 0);
        enable_input : in std_logic
    );
end entity;

architecture behavior of inputunit is

signal memorisebits : std_logic_vector(7 downto 0);

begin
    process(enable_input)
    begin
        if (enable_input = '1') then
            memorisebits <= readbits;
        end if;
        
        storebits <= memorisebits;

    end process;
end architecture;