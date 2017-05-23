// //  require twitter/typeahead
//
//
//
// $(window).ready(() => {
//     // let players = new Bloodhound({
//     //     datumTokenizer: Bloodhound.tokenizers.obj.whitespace('value'),
//     //     queryTokenizer: Bloodhound.tokenizers.whitespace,
//     //     local: ['Andy', 'Gilles'],
//     //     remote: {
//     //         url: '/players/load_suggestions?search=%QUERY',
//     //         wildcard: '%QUERY',
//     //         transform: response => {
//     //             console.log(response.map(d => d.name));
//     //             return response.map(d => d.name);
//     //         }
//     //     },
//     // });
//
//     function lookForSuggestions(query, callback) {
//         $.ajax({
//             type: 'GET',
//             url: '/players/load_suggestions',
//             data: {search: query},
//             success: response => {
//                 callback(response.map(d => d.name));
//             },
//         });
//     }
//
//     $('.typeahead').autocomplete(null, {
//         source: lookForSuggestions,
//         name: 'players',
//         // display: 'value',
//         templates: {
//             suggestion: function(suggestion) {
//                 return suggestion;
//             }
//         }
//     });
// });
