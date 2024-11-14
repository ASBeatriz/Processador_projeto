library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity reg4bits is
    port(
        clk, reset : in std_logic;
        entradas : in std_logic_vector(3 downto 0);
        qvector, qnvector : out std_logic_vector(3 downto 0)
    );
end entity;

architecture behavior of reg4bits is

signal qsigvec : std_logic_vector(3 downto 0);
signal qnsigvec : std_logic_vector(3 downto 0);

begin
    process(clk, reset)
    begin
        if(reset = '0') then
            qsigvec <= (others => '0');
            qnsigvec <= (others => '1');
        elsif (rising_edge(clk)) then
            qsigvec <= entradas;
            qnsigvec <= not entradas;
        end if;

        qvector <= qsigvec;
        qnvector <= qnsigvec;

    end process;
end architecture;